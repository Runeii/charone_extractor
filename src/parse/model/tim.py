from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from io import BytesIO
from src.utils.binary_reader import BinaryReader

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
    header: TIMHeader = field(init=False)
    image_data: bytes = field(init=False)
    palette_data: Optional[bytes] = field(init=False)
    palette_colors: Optional[List[Tuple[float, float, float, float]]] = field(init=False)  # RGBA colors


    MAGIC_NUMBER = b'\x10\x00\x00\x00'
    
    def __post_init__(self):
        self.stream = BytesIO(self.data)

        self.parse()

        if self.header.has_palette and self.palette_data is None:
            raise ValueError("Palette data is missing")
        
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
            
            # Parse palette colors with proper alpha handling
            self.palette_colors = []
            for i in range(0, len(palette_data), 2):
                if i + 1 >= len(palette_data):
                    break
                    
                word = palette_data[i] | (palette_data[i+1] << 8)
                
                # Extract BGR555 components
                b = ((word >> 10) & 0x1F) / 31.0
                g = ((word >>  5) & 0x1F) / 31.0
                r = ( word        & 0x1F) / 31.0
                a = 0.0 if (word >> 15) else 1.0
                
                self.palette_colors.append((r, g, b, a))

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

        if has_palette:
          self.palette_data = palette_data
        
        return True