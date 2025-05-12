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
            image = bpy.data.images.new(f"{model_name}-{i}", tim.header.img_w, tim.header.img_h)  # type: ignore[attr-defined]
            
            # Convert TIM data to RGBA pixels
            pixels = self._convert_tim_to_pixels(tim)
            
            # Set image pixels using foreach_set for efficiency and type safety
            image.pixels.foreach_set(list(pixels))  # type: ignore[attr-defined]
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
        nodes = material.node_tree.nodes  # type: ignore[attr-defined]
        links = material.node_tree.links  # type: ignore[attr-defined]
        
        # Clear default nodes
        nodes.clear()  # type: ignore[attr-defined]
        
        # Create output node
        output = nodes.new('ShaderNodeOutputMaterial')  # type: ignore[attr-defined]
        output.location = (300, 0)
        
        # Create shader node
        shader = nodes.new('ShaderNodeBsdfPrincipled')  # type: ignore[attr-defined]
        shader.location = (0, 0)
        
        # Connect shader to output
        links.new(shader.outputs['BSDF'], output.inputs['Surface'])  # type: ignore[attr-defined]
        
        last_color = None
        last_alpha = None
        
        for i, image in enumerate(images):
            tex = nodes.new('ShaderNodeTexImage')  # type: ignore[attr-defined]
            tex.image = image  # type: ignore[attr-defined]
            tex.extension = 'CLIP'  # type: ignore[attr-defined]
            tex.location = (-300, -i * 200)
            
            if i == 0:
                links.new(tex.outputs['Color'], shader.inputs['Base Color'])  # type: ignore[attr-defined]
                links.new(tex.outputs['Alpha'], shader.inputs['Alpha'])  # type: ignore[attr-defined]
                last_color = tex
                last_alpha = tex
            else:
                mix_color = nodes.new('ShaderNodeMixRGB')  # type: ignore[attr-defined]
                mix_color.blend_type = 'MIX'  # type: ignore[attr-defined]
                mix_color.location = (-150, -i * 200)
                links.new(last_color.outputs['Color'], mix_color.inputs[1])  # type: ignore[attr-defined]
                links.new(tex.outputs['Color'], mix_color.inputs[2])  # type: ignore[attr-defined]
                links.new(mix_color.outputs['Color'], shader.inputs['Base Color'])  # type: ignore[attr-defined]
                last_color = mix_color

                mix_alpha = nodes.new('ShaderNodeMixRGB')  # type: ignore[attr-defined]
                mix_alpha.blend_type = 'MIX'  # type: ignore[attr-defined]
                mix_alpha.location = (-150, -i * 200 - 100)
                links.new(last_alpha.outputs['Alpha'], mix_alpha.inputs[1])  # type: ignore[attr-defined]
                links.new(tex.outputs['Alpha'], mix_alpha.inputs[2])  # type: ignore[attr-defined]
                links.new(mix_alpha.outputs['Color'], shader.inputs['Alpha'])  # type: ignore[attr-defined]
                last_alpha = mix_alpha
        
        return material
    
    def _convert_tim_to_pixels(self, tim: TIM) -> List[float]:
        """
        Converts TIM texture data to RGBA pixels
        
        Args:
            tim: TIM texture data
            
        Returns:
            List of RGBA values (0-1) for each pixel
        """
        pixels: List[float] = []
        
        if tim.palette_data:
            # Indexed color mode
            palette: List[List[float]] = self._parse_palette(tim.palette_data, tim.header.bpp)
            
            # Convert image data using palette
            for byte in tim.image_data:
                if tim.header.bpp == 4:  # 4-bit indexed
                    # Each byte contains two pixels
                    for i in range(2):
                        index = (byte >> (4 * (1-i))) & 0x0F
                        if index < len(palette):
                            pixels.extend(palette[index])  # type: ignore[reportGeneralTypeIssues]
                        else:
                            pixels.extend([0, 0, 0, 0])  # type: ignore[reportGeneralTypeIssues]
                else:  # 8-bit indexed
                    if byte < len(palette):
                        pixels.extend(palette[byte])  # type: ignore[reportGeneralTypeIssues]
                    else:
                        pixels.extend([0, 0, 0, 0])  # type: ignore[reportGeneralTypeIssues]
        else:
            # Direct color mode
            for i in range(0, len(tim.image_data), 2):
                if i + 1 < len(tim.image_data):
                    color = (tim.image_data[i] << 8) | tim.image_data[i + 1]
                    # Convert 16-bit color to RGBA
                    r = ((color >> 10) & 0x1F) / 31.0
                    g = ((color >> 5) & 0x1F) / 31.0
                    b = (color & 0x1F) / 31.0
                    a = 1.0 if (color >> 15) else 0.0
                    pixels.extend([r, g, b, a])  # type: ignore[reportGeneralTypeIssues]
        
        return pixels
    
    def _parse_palette(self, palette_data: bytes, bpp: int) -> List[List[float]]:
        """
        Parses TIM palette data into RGBA colors
        
        Args:
            palette_data: Raw palette data
            bpp: Bits per pixel (4 or 8)
            
        Returns:
            List of RGBA colors (0-1)
        """
        palette: List[List[float]] = []
        entries = 16 if bpp == 4 else 256
        
        for i in range(0, len(palette_data), 2):
            if len(palette) >= entries:
                break
                
            if i + 1 < len(palette_data):
                color = (palette_data[i] << 8) | palette_data[i + 1]
                # Convert 16-bit color to RGBA
                r = ((color >> 10) & 0x1F) / 31.0
                g = ((color >> 5) & 0x1F) / 31.0
                b = (color & 0x1F) / 31.0
                a = 1.0 if (color >> 15) else 0.0
                palette.append([r, g, b, a])  # type: ignore[reportGeneralTypeIssues]
        
        return palette 