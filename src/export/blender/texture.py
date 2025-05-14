import bpy
from bpy.types import Image
from typing import List
from src.parse.model.tim import TIM

class BlenderTextureExporter:
    """Handles creation and setup of Blender textures and materials"""
    
    def create_textures(self, textures: List[TIM], model_name: str) -> List[bpy.types.Image]:
        """
        Creates Blender images from TIM textures
        
        Args:
            textures: List of TIM textures
            model_name: Name of the model
            
        Returns:
            List of created Blender images
        """
        blender_images: List[Image] = []
        
        for i, tim in enumerate(textures):
          # Create new image
          image = bpy.data.images.new(f"{model_name}-{i}", tim.header.img_w, tim.header.img_h)
          
          # Convert TIM data to RGBA pixels
          pixels = self._convert_tim_to_pixels(tim)
          
          # Set image pixels using foreach_set for efficiency and type safety
          image.pixels.foreach_set(list(pixels))
          image.use_fake_user = True  # Keep image in memory
          blender_images.append(image)
            
        return blender_images
    
    def create_material(self, model_name: str, images: List[bpy.types.Image]) -> bpy.types.Material:
        """
        Creates a Blender material with nodes for the textures
        
        Args:
            model_name: Name of the model
            images: List of Blender images to use as textures
            
        Returns:
            Created Blender material
        """
        # Create material
        material = bpy.data.materials.new(model_name)
        material.use_nodes = True
        material.blend_method = 'HASHED'  # For transparency
        
        # Get node tree
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        # Clear default nodes
        nodes.clear()
        
        # Create output node
        output_node = nodes.new('ShaderNodeOutputMaterial')
        
        # Create shader node
        shader_node = nodes.new('ShaderNodeBsdfPrincipled')
        shader_node.location[0] = output_node.location[0] - 300
        shader_node.location[1] = output_node.location[1]
        
        # Create uv node
        uv_node = nodes.new("ShaderNodeUVMap")
        uv_node.location[0] = shader_node.location[0]-1000
        uv_node.location[1] = shader_node.location[1]
        
        # Connect shader to output
        links.new(shader_node.outputs['BSDF'], output_node.inputs['Surface']) 
        
        last_color = None
        last_alpha = None

        for i, image in enumerate(images):
            texture_node = nodes.new('ShaderNodeTexImage')
            texture_node.image = image
            texture_node.extension = 'CLIP'
            texture_node.location[0]=shader_node.location[0]-500
            texture_node.location[1]=shader_node.location[1]- i*500
            texture_node.name="texture{}".format(i)

            mapping_node=nodes.new("ShaderNodeMapping")
            mapping_node.vector_type='TEXTURE'
            mapping_node.inputs[1].default_value[1] = i
            mapping_node.location[0]=texture_node.location[0]-200
            mapping_node.location[1]=texture_node.location[1]
            mapping_node.name="mapping{}".format(i)

            material.node_tree.links.new(uv_node.outputs[0], mapping_node.inputs[0])
            material.node_tree.links.new(mapping_node.outputs[0], texture_node.inputs[0])
                    
            if i == 0:
                links.new(texture_node.outputs['Color'], shader_node.inputs['Base Color'])
                links.new(texture_node.outputs['Alpha'], shader_node.inputs['Alpha'])
                last_color = texture_node
                last_alpha = texture_node
            else:
                mix_color = nodes.new('ShaderNodeMixRGB')
                mix_color.blend_type = 'MIX'
                mix_color.location = (-150, -i * 200)
                links.new(last_color.outputs['Color'], mix_color.inputs[1])
                links.new(texture_node.outputs['Color'], mix_color.inputs[2])
                links.new(mix_color.outputs['Color'], shader_node.inputs['Base Color'])
                last_color = mix_color


                mix_alpha = nodes.new('ShaderNodeMixRGB')
                mix_alpha.blend_type = 'MIX'
                mix_alpha.location = (-150, -i * 200 - 100)
                links.new(last_alpha.outputs['Alpha'], mix_alpha.inputs[1])
                links.new(last_alpha.outputs['Color'], mix_alpha.inputs[1])
                links.new(texture_node.outputs['Color'],         mix_alpha.inputs[2])
                links.new(texture_node.outputs['Alpha'],         mix_alpha.inputs['Fac'])
                links.new(mix_alpha.outputs['Color'],   shader_node.inputs['Alpha'])
                last_alpha = mix_alpha
        
        return material
    def _convert_tim_to_pixels(self, tim: TIM) -> List[float]:
        """
        Converts TIM texture data to RGBA pixels, bottom-up,
        forcing any non-black color to alpha=1.
        Corrected so channels use PS1's BGR555 ordering.
        """
        w, h = tim.header.img_w, tim.header.img_h

        # 1) Build palette lookup: index -> (r,g,b,a)
        palette: List[List[float]] = []
        if tim.palette_data:
            data = tim.palette_data
            for i in range(0, len(data), 2):
                word = data[i] | (data[i+1] << 8)
                # PS1 BGR555: bits10–14=Blue, bits5–9=Green, bits0–4=Red
                b = ((word >> 10) & 0x1F) / 31.0
                g = ((word >>  5) & 0x1F) / 31.0
                r = ( word        & 0x1F) / 31.0
                a = 1.0 if (word >> 15) else 0.0
                palette.append([r, g, b, a])

        # 2) Decode all indices
        indices: List[int]
        if tim.header.bpp == 0:  # 4-bit
            indices = []
            for byte in tim.image_data:
                indices.append((byte >> 4) & 0x0F)
                indices.append(byte & 0x0F)
        else:                    # 8-bit
            indices = list(tim.image_data)

        # ensure exactly w*h entries
        total = w * h
        if len(indices) < total:
            indices += [0] * (total - len(indices))
        else:
            indices = indices[:total]

        # 3) Allocate RGBA list
        pixels = [0.0] * (w * h * 4)

        # 4) Write bottom-up
        for y in range(h):
            dst_row = h - 1 - y
            for x in range(w):
                idx = indices[y * w + x]
                if idx < len(palette):
                    r, g, b, a = palette[idx]
                else:
                    r = g = b = a = 0.0

                # force any non-black → opaque
                if (r, g, b) != (0.0, 0.0, 0.0):
                    a = 1.0

                dst = (dst_row * w + x) * 4
                pixels[dst    ] = r
                pixels[dst + 1] = g
                pixels[dst + 2] = b
                pixels[dst + 3] = a

        return pixels
