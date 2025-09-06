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
          image = bpy.data.images.new(f"{model_name}-{i}", tim.header.img_w, tim.header.img_h, alpha=True)
          
          # Convert TIM data to RGBA pixels
          pixels = self._convert_tim_to_pixels(tim)
          
          # Set image pixels using foreach_set for efficiency and type safety
          image.pixels.foreach_set(list(pixels))
          image.use_fake_user = True  # Keep image in memory
          
          # Pack the image data into the blend file to ensure it persists when saved
          image.pack()
          
          blender_images.append(image)
            
        return blender_images
    
    def create_materials(self, model_name: str, images: List[bpy.types.Image]) -> List[bpy.types.Material]:
        """
        Creates a Blender material for each texture
        
        Args:
            model_name: Name of the model
            images: List of Blender images to use as textures
            
        Returns:
            List of created Blender materials
        """
        materials = []
        
        for i, image in enumerate(images):
            # Create material
            material = bpy.data.materials.new(f"{model_name}_texture_{i}")
            material.use_nodes = True
            
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
            
            # Create texture node
            texture_node = nodes.new('ShaderNodeTexImage')
            texture_node.image = image
            texture_node.extension = 'REPEAT'
            texture_node.location[0] = shader_node.location[0]-500
            texture_node.location[1] = shader_node.location[1]
            
            # Create mapping node
            mapping_node = nodes.new("ShaderNodeMapping")
            mapping_node.vector_type = 'TEXTURE'
            mapping_node.inputs[1].default_value[1] = i
            mapping_node.location[0] = texture_node.location[0]-200
            mapping_node.location[1] = texture_node.location[1]
            mapping_node.name = f"mapping_{i}"
            
            # Connect nodes
            links.new(uv_node.outputs[0], mapping_node.inputs[0])
            links.new(mapping_node.outputs[0], texture_node.inputs[0])
            links.new(texture_node.outputs['Color'], shader_node.inputs['Base Color'])
            links.new(texture_node.outputs['Alpha'], shader_node.inputs['Alpha'])
            links.new(shader_node.outputs['BSDF'], output_node.inputs['Surface'])
            
            material.blend_method = 'CLIP'  # Use alpha clip for sharp transparency
            
            materials.append(material)
        
        return materials

    def _convert_tim_to_pixels(self, tim: TIM) -> List[float]:
        """
        Converts TIM texture data to RGBA pixels, bottom-up.
        Uses pre-parsed palette colors from TIM class.
        """
        w, h = tim.header.img_w, tim.header.img_h

        # Use pre-parsed palette colors
        palette = tim.palette_colors if tim.palette_colors else []

        # Decode all indices
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

        # Allocate RGBA list
        pixels = [0.0] * (w * h * 4)

        # Write bottom-up
        for y in range(h):
            dst_row = h - 1 - y
            for x in range(w):
                idx = indices[y * w + x]
                if idx < len(palette):
                    r, g, b, a = palette[idx]  # Use pre-parsed colors
                else:
                  r = g = b = a = 0.0

                dst = (dst_row * w + x) * 4
                pixels[dst    ] = r
                pixels[dst + 1] = g
                pixels[dst + 2] = b
                pixels[dst + 3] = a

        return pixels
