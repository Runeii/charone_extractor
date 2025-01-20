from dataclasses import dataclass, field
from typing import List, Optional
from io import BytesIO
from PIL import Image
import os
from ...utils.binary_reader import BinaryReader

@dataclass
class TIMHeader:
    bpp: int
    has_palette: bool
    img_size: int
    img_x: int
    img_y: int
    img_w: int
    img_h: int
    pal_size: Optional[int]
    pal_x: Optional[int]
    pal_y: Optional[int]
    pal_w: Optional[int]
    pal_h: Optional[int]
    nb_pal: Optional[int]



@dataclass
class TIM:
    name: str
    data: bytes

    stream: BytesIO = field(init=False)
    header: Optional[TIMHeader] = field(init=False)
    image_data: Optional[bytes] = field(init=False)
    palette_data: Optional[bytes] = field(init=False)


    MAGIC_NUMBER = b'\x10\x00\x00\x00'
    
    def __post_init__(self):
        self.stream = BytesIO(self.data)
        self.header: Optional[TIMHeader] = None
        self.image_data: Optional[bytes] = None
        self.palette_data: Optional[bytes] = None

        self.parse()
        
    def __str__(self):
        if not self.header:
            return f"Model {self.name} (unparsed)"
            
        result = [f"Model {self.name}"]
        result.append(f"  BPP: {self.header.bpp}")
        result.append(f"  Has Palette: {self.header.has_palette}")
        result.append(f"  Image: {self.header.img_w}x{self.header.img_h} at ({self.header.img_x},{self.header.img_y})")
        
        if self.header.has_palette:
            result.append(f"  Palette: {self.header.pal_w}x{self.header.pal_h} at ({self.header.pal_x},{self.header.pal_y})")
            result.append(f"  Num Palettes: {self.header.nb_pal}")
            
        return "\n".join(result)

    def parse(self) -> bool:
        """
        Parse TIM data
        Returns:
            bool: True if successful
        """        
        # Check magic number
        if self.stream.read(4) != self.MAGIC_NUMBER:
            print("Invalid TIM magic number")
            return False
            
        # Read flags byte
        flags = ord(self.stream.read(1))
        bpp = flags & 0x03
        has_palette = bool((flags >> 3) & 1)
        
        # Skip 3 bytes
        self.stream.read(3)
        
        if has_palette and bpp > 1:
            print(f"Invalid TIM flags: bpp={bpp}, has_palette={has_palette}")
            return False
            
        # Parse palette if present
        pal_size = None
        pal_x = pal_y = pal_w = pal_h = nb_pal = None
        palette_data = None
        
        if has_palette:
            pal_size = BinaryReader.read_uint32(self.stream)
            
            # Read palette header
            pal_x = BinaryReader.read_uint16(self.stream)
            pal_y = BinaryReader.read_uint16(self.stream)
            pal_w = BinaryReader.read_uint16(self.stream)
            pal_h = BinaryReader.read_uint16(self.stream)
            
            # Calculate palette entries
            one_pal_size = 16 if bpp == 0 else 256
            nb_pal = (pal_size - 12) // (one_pal_size * 2)
            if (pal_size - 12) % (one_pal_size * 2) != 0:
                nb_pal *= 2
                
            if nb_pal <= 0:
                return False
                
            # Read palette data
            palette_data = self.stream.read(pal_size - 12)

        # Read image header
        img_size = BinaryReader.read_uint32(self.stream)
        img_x = BinaryReader.read_uint16(self.stream)
        img_y = BinaryReader.read_uint16(self.stream)
        img_w = BinaryReader.read_uint16(self.stream)
        img_h = BinaryReader.read_uint16(self.stream)
        
        # Adjust width based on bpp
        if bpp == 0:
            img_w *= 4
        elif bpp == 1:
            img_w *= 2
            
        # Store the header information
        self.header = TIMHeader(
            bpp=bpp,
            has_palette=has_palette,
            img_size=img_size,
            img_x=img_x,
            img_y=img_y,
            img_w=img_w,
            img_h=img_h,
            pal_size=pal_size,
            pal_x=pal_x,
            pal_y=pal_y,
            pal_w=pal_w,
            pal_h=pal_h,
            nb_pal=nb_pal
        )
        
        # Read image data
        self.image_data = self.stream.read(img_size - 12)
        self.palette_data = palette_data
        
        return True

    def create_image(self) -> Optional[Image.Image]:
        """
        Create a PIL Image from the parsed TIM data
        Returns:
            Optional[Image.Image]: The created image, or None if creation fails
        """
        if not self.header or not self.image_data:
            print("Cannot create image - TIM not properly parsed")
            return None
            
        if self.header.bpp == 0:  # 4-bit
            image = Image.new('P', (self.header.img_w, self.header.img_h))
            pixels = []
            
            # Process 4-bit data (2 pixels per byte)
            for byte in self.image_data:
                pixels.append(byte >> 4)
                pixels.append(byte & 0x0F)
            
            if self.header.has_palette and self.palette_data:
                palette = []
                pal_stream = BytesIO(self.palette_data)
                for _ in range(16):
                    color = BinaryReader.read_uint16(pal_stream)
                    r = (color & 0x1F) << 3
                    g = ((color >> 5) & 0x1F) << 3
                    b = ((color >> 10) & 0x1F) << 3
                    palette.extend([r, g, b])
                image.putpalette(palette)
                
            image.putdata(pixels[:self.header.img_w * self.header.img_h])
            
        elif self.header.bpp == 1:  # 8-bit
            image = Image.new('P', (self.header.img_w, self.header.img_h))
            pixels = list(self.image_data)
            
            if self.header.has_palette and self.palette_data:
                palette = []
                pal_stream = BytesIO(self.palette_data)
                for _ in range(256):
                    color = BinaryReader.read_uint16(pal_stream)
                    r = (color & 0x1F) << 3
                    g = ((color >> 5) & 0x1F) << 3
                    b = ((color >> 10) & 0x1F) << 3
                    palette.extend([r, g, b])
                image.putpalette(palette)
                
            image.putdata(pixels[:self.header.img_w * self.header.img_h])
            
        else:  # 16-bit direct color
            image = Image.new('RGB', (self.header.img_w, self.header.img_h))
            pixels = []
            for i in range(0, len(self.image_data), 2):
                color = self.image_data[i] | (self.image_data[i+1] << 8)
                r = (color & 0x1F) << 3
                g = ((color >> 5) & 0x1F) << 3
                b = ((color >> 10) & 0x1F) << 3
                pixels.append((r, g, b))
            image.putdata(pixels)
            
        return image

    def save(self, output_path: str) -> bool:
        """
        Save TIM data as both raw TIM format and PNG image
        Args:
            output_path: Path for the output files (extension will be added)
        Returns:
            bool: True if successful
        """
        if not self.header or not self.image_data:
            print("Cannot save - TIM not properly parsed")
            return False
            
        # Create and save PNG
        image = self.create_image()
        if not image:
            return False
            
        os.makedirs(output_path, exist_ok=True)
        png_path = f"{output_path}/{self.name}.png"
        image.save(png_path)

        # Create raw TIM format
        tim_data = bytearray()
        
        # Header
        tim_data.extend(self.MAGIC_NUMBER)
        flag = (self.header.has_palette << 3) | (self.header.bpp & 3)
        tim_data.extend(flag.to_bytes(4, 'little'))
        
        if self.header.has_palette and self.palette_data:
            # Palette section
            tim_data.extend(self.header.pal_size.to_bytes(4, 'little'))
            tim_data.extend(self.header.pal_x.to_bytes(2, 'little'))
            tim_data.extend(self.header.pal_y.to_bytes(2, 'little'))
            tim_data.extend(self.header.pal_w.to_bytes(2, 'little'))
            tim_data.extend(self.header.pal_h.to_bytes(2, 'little'))
            tim_data.extend(self.palette_data)

        # Image section
        save_width = self.header.img_w
        if self.header.bpp == 0:
            save_width //= 4
        elif self.header.bpp == 1:
            save_width //= 2
            
        tim_data.extend(self.header.img_size.to_bytes(4, 'little'))
        tim_data.extend(self.header.img_x.to_bytes(2, 'little'))
        tim_data.extend(self.header.img_y.to_bytes(2, 'little'))
        tim_data.extend(save_width.to_bytes(2, 'little'))
        tim_data.extend(self.header.img_h.to_bytes(2, 'little'))
        tim_data.extend(self.image_data)

        # Save TIM file
        tim_path = f"{output_path}/{self.name}.tim"
        with open(tim_path, 'wb') as f:
            f.write(tim_data)

        print(f"Save TIM successful - PNG: {png_path}, TIM: {tim_path}")
        return True