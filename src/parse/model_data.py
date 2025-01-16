import struct
from dataclasses import dataclass
from typing import List
from .face import Face
from .bone import Bone
from .vertex import Vertex
from .skin_object import SkinObject
from .unknown_data_object import UnknownDataObject
from .texture_animation import TextureAnimation
from io import BytesIO

@dataclass
class ModelData:
  name: str
  data: bytes
  offset: int
  bones: List[Bone] = None
  texture_animations: List[TextureAnimation] = None
  faces: List[Face] = None
  vertices: List[Vertex] = None
  skin_objects: List[SkinObject] = None
  unknown_data_objects: List[UnknownDataObject] = None

  def __init__(self, name: str, data: bytes, offset: int):
    self.name = name
    self.data = data
    self.offset = offset
    self.parse()

  @staticmethod
  def read_uint32(stream: BytesIO) -> int:
      return struct.unpack("<I", stream.read(4))[0]
    
  @staticmethod
  def read_uint16(stream: BytesIO) -> int:
      return struct.unpack("<H", stream.read(2))[0]
  
  @staticmethod
  def read_int16(stream: BytesIO) -> int:
      return struct.unpack("<h", stream.read(2))[0]

  def parse(self):
    stream = BytesIO(self.data[self.offset:])
    
    number_of_bones = self.read_uint32(stream)
    number_of_vertices = self.read_uint32(stream)
    number_of_texture_animations = self.read_uint32(stream)
    number_of_faces = self.read_uint32(stream)
    number_of_unknown_data_objects = self.read_uint32(stream)
    number_of_skin_objects = self.read_uint32(stream)

    __unknown = self.read_uint32(stream)

    triangle_count = self.read_uint32(stream)
    quad_count = self.read_uint32(stream)
    
    offset_of_bones = self.read_uint32(stream)
    offset_of_vertices = self.read_uint32(stream)
    offset_of_texture_animations = self.read_uint32(stream)
    offset_of_faces = self.read_uint32(stream)
    offset_of_unknown_data_objects = self.read_uint32(stream)
    offset_of_skin_objects = self.read_uint32(stream)
    offset_of_animation_data = self.read_uint32(stream)

    __unknown2 = self.read_uint32(stream)

    self.bones = self.parse_bones(number_of_bones, offset_of_bones)
    self.texture_animations = self.parse_texture_animations(number_of_texture_animations, offset_of_texture_animations)
    self.faces = self.parse_faces(number_of_faces, offset_of_faces)
    self.vertices = self.parse_vertices(number_of_vertices, offset_of_vertices)
    self.skin_objects = self.parse_skin_objects(number_of_skin_objects, offset_of_skin_objects)
    self.unknown_data_objects = self.parse_unknown_data_objects(number_of_unknown_data_objects, offset_of_unknown_data_objects)

    print(offset_of_skin_objects, self.unknown_data_objects[0].start_skinobject_index + offset_of_skin_objects)
  
  def parse_bones(self, number_of_bones: int, offset_of_bones: int):
    stream = BytesIO(self.data[offset_of_bones:])
    bones = []
    for i in range(number_of_bones):
      bone_data = stream.read(64)
      bone = Bone(bone_data)
      bones.append(bone)
    
    return bones
  
  def parse_texture_animations(self, number_of_texture_animations: int, offset_of_texture_animations: int):
    stream = BytesIO(self.data[offset_of_texture_animations:])
    texture_animations = []
    for i in range(number_of_texture_animations):
      texture_animation_data = stream.read(64)
      texture_animation = TextureAnimation(texture_animation_data)
      texture_animations.append(texture_animation)
    
    return texture_animations
  
  def parse_faces(self, number_of_faces: int, offset_of_faces: int):
    stream = BytesIO(self.data[offset_of_faces:])
    faces = []
    for i in range(number_of_faces):
      face_data = stream.read(64)
      face = Face(face_data)
      faces.append(face)

    return faces
  
  def parse_vertices(self, number_of_vertices: int, offset_of_vertices: int):
    stream = BytesIO(self.data[offset_of_vertices:])
    vertices = []
    for i in range(number_of_vertices):
      vertex_data = stream.read(24)
      vertex = Vertex(vertex_data)
      vertices.append(vertex)

    return vertices
  
  def parse_skin_objects(self, number_of_skin_objects: int, offset_of_skin_objects: int):
    stream = BytesIO(self.data[offset_of_skin_objects:])
    skin_objects = []
    for i in range(number_of_skin_objects):
      skin_object_data = stream.read(64)
      skin_object = SkinObject(skin_object_data)
      skin_objects.append(skin_object)
    
    return skin_objects

  def parse_unknown_data_objects(self, number_of_unknown_data_objects: int, offset_of_unknown_data_objects: int):
    stream = BytesIO(self.data[offset_of_unknown_data_objects:])
    unknown_data_objects = []
    for i in range(number_of_unknown_data_objects):
      unknown_data_object_data = stream.read(32)
      unknown_data_object = UnknownDataObject(unknown_data_object_data)
      unknown_data_objects.append(unknown_data_object)
    
    return unknown_data_objects
