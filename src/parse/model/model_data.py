from dataclasses import dataclass, field
from typing import List
from .face import Face
from .bone import Bone
from .vertex import Vertex
from .skin_object import SkinObject
from .unknown_data_object import UnknownDataObject
from .texture_animation import TextureAnimation
from io import BytesIO
from .animations.__parser import AnimationsParser
from ...utils.binary_reader import BinaryReader

@dataclass
class ModelData:
  data: bytes
  name: str
  offset: int

  char_one_data: bytes | None = field(default=None)

  bones: List[Bone] = field(init=False)
  texture_animations: List[TextureAnimation] = field(init=False)
  faces: List[Face] = field(init=False)
  vertices: List[Vertex] = field(init=False)
  skin_objects: List[SkinObject] = field(init=False)
  unknown_data_objects: List[UnknownDataObject] = field(init=False)

  def __post_init__(self):
    stream = BytesIO(self.data[self.offset:])
    
    number_of_bones = BinaryReader.read_uint32(stream)
    number_of_vertices = BinaryReader.read_uint32(stream)
    number_of_texture_animations = BinaryReader.read_uint32(stream)
    number_of_faces = BinaryReader.read_uint32(stream)
    number_of_unknown_data_objects = BinaryReader.read_uint32(stream)
    number_of_skin_objects = BinaryReader.read_uint32(stream)

    __unknown = BinaryReader.read_uint32(stream)
    
    triangle_count = BinaryReader.read_uint16(stream)
    quad_count = BinaryReader.read_uint16(stream)

    if triangle_count + quad_count != number_of_faces:
      raise ValueError("Triangle and quad counts do not match total face count")

    offset_of_bones = BinaryReader.read_uint32(stream) + self.offset
    offset_of_vertices = BinaryReader.read_uint32(stream) + self.offset
    offset_of_texture_animations = BinaryReader.read_uint32(stream) + self.offset
    offset_of_faces = BinaryReader.read_uint32(stream) + self.offset
    offset_of_unknown_data_objects = BinaryReader.read_uint32(stream) + self.offset
    offset_of_skin_objects = BinaryReader.read_uint32(stream) + self.offset
    offset_of_animation_data = BinaryReader.read_uint32(stream) + self.offset

    __unknown2 = BinaryReader.read_uint32(stream)

    self.bones = self.parse_bones(number_of_bones, offset_of_bones)
    self.texture_animations = self.parse_texture_animations(number_of_texture_animations, offset_of_texture_animations)
    self.faces = self.parse_faces(number_of_faces, offset_of_faces)
    self.vertices = self.parse_vertices(number_of_vertices, offset_of_vertices)
    self.skin_objects = self.parse_skin_objects(number_of_skin_objects, offset_of_skin_objects)
    self.unknown_data_objects = self.parse_unknown_data_objects(number_of_unknown_data_objects, offset_of_unknown_data_objects)

    # When working with main character models, we're constructing the model data from a separate MCH file
    # Animations remain within the chara.one file.
    animation_data = self.char_one_data if self.char_one_data else self.data[offset_of_animation_data:]

    self.animations = AnimationsParser(model_name=self.name, data=animation_data)

  def parse_bones(self, number_of_bones: int, offset_of_bones: int) -> List[Bone]:
    stream = BytesIO(self.data[offset_of_bones:])
    bones: List[Bone] = []
    for _ in range(number_of_bones):
      bone_data = stream.read(64)
      bone = Bone(bone_data)
      bones.append(bone)

    return bones
  
  def parse_texture_animations(self, number_of_texture_animations: int, offset_of_texture_animations: int) -> List[TextureAnimation]:
    stream = BytesIO(self.data[offset_of_texture_animations:])
    texture_animations: List[TextureAnimation] = []
    for _ in range(number_of_texture_animations):
      texture_animation = TextureAnimation(stream)
      texture_animations.append(texture_animation)
    
    return texture_animations
  
  def parse_faces(self, number_of_faces: int, offset_of_faces: int) -> List[Face]:
    stream = BytesIO(self.data[offset_of_faces:])

    faces: List[Face] = []
    for _ in range(number_of_faces):
      face_data = stream.read(64)
      face = Face(face_data)
      faces.append(face)

    return faces
  
  def parse_vertices(self, number_of_vertices: int, offset_of_vertices: int) -> List[Vertex]:
    stream = BytesIO(self.data[offset_of_vertices:])
    vertices: List[Vertex] = []
    for _ in range(number_of_vertices):
      vertex_data = stream.read(24)
      vertex = Vertex(vertex_data)
      vertices.append(vertex)

    return vertices
  
  def parse_skin_objects(self, number_of_skin_objects: int, offset_of_skin_objects: int) -> List[SkinObject]:
    stream = BytesIO(self.data[offset_of_skin_objects:])
    skin_objects: List[SkinObject] = []
    for _ in range(number_of_skin_objects):
      skin_object_data = stream.read(8)
      skin_object = SkinObject(skin_object_data)
      skin_objects.append(skin_object)
    
    return skin_objects

  def parse_unknown_data_objects(self, number_of_unknown_data_objects: int, offset_of_unknown_data_objects: int) -> List[UnknownDataObject]:
    stream = BytesIO(self.data[offset_of_unknown_data_objects:])
    unknown_data_objects: List[UnknownDataObject] = []
    for _ in range(number_of_unknown_data_objects):
      unknown_data_object_data = stream.read(32)
      unknown_data_object = UnknownDataObject(unknown_data_object_data)
      unknown_data_objects.append(unknown_data_object)
    
    return unknown_data_objects
