from dataclasses import dataclass, field
from typing import List
from ..parse.parsed_model import ParsedModel
from ..parse.tim import TIM
from ..parse.bone import Bone
from ..parse.texture_animation import TextureAnimation
from ..parse.face import Face
from ..parse.vertex import Vertex
from ..parse.skin_object import SkinObject
from ..parse.unknown_data_object import UnknownDataObject

from .sanitised_face import SanitisedFace
from .uv import UV
from .sanitised_bone import SanitisedBone

@dataclass
class SanitisedModel:
  model: ParsedModel

  id: int = field(init=None)
  name: str = field(init=None)
  tim: TIM = field(init=None)
  bones: List[Bone] = field(init=None)
  texture_animations: List[TextureAnimation] = field(init=None)
  faces: List[Face] = field(init=None)
  vertices: List[Vertex] = field(init=None)
  skin_objects: List[SkinObject] = field(init=None)
  unknown_data_objects: List[UnknownDataObject] = field(init=None)

  sanitised_faces: List[SanitisedFace] = field(init=None)
  uvs: List[UV] = field(init=None)

  def __post_init__(self):
    self.id = self.model.id
    self.name = self.model.name

    self.tim = self.model.tim
    self.tim.save(f"output/{self.name}.png")

    self.bones = self.model.model_data.bones
    self.texture_animations = self.model.model_data.texture_animations
    self.faces = self.model.model_data.faces
    self.vertices = self.model.model_data.vertices
    self.skin_objects = self.model.model_data.skin_objects
    self.unknown_data_objects = self.model.model_data.unknown_data_objects

    self.sanitise_bones()
    self.sanitise_vertices()
    self.sanitise_faces()


  def sanitise_bones(self):
    self.bones = list(map(lambda bone : SanitisedBone(bone), self.bones))
    

  def sanitise_vertices(self):
    """From MCH2Blend, scale and detect negatives
    
    Structure:
    - x (2 bytes): SHORT - X position scaled by 1/256
    - y (2 bytes): SHORT - Y position scaled by 1/256
    - z (2 bytes): SHORT - Z position scaled by 1/256
    Note: Coordinates use 16-bit values with MAX_SIZE = 4096 for negative detection
    """
    MAX_SIZE = 4096

    def sanitise_coord(value: int) -> float:
      if value > 65536 - MAX_SIZE:  # if value > 61440
          value -= 65536
      return value / 256

    def sanitise(vertex: Vertex):
      vertex.x = sanitise_coord(vertex.x)
      vertex.y = sanitise_coord(vertex.y)
      vertex.z = sanitise_coord(vertex.z)
      return vertex

    self.vertices = list(map(sanitise, self.vertices))


  def sanitise_faces(self):
    sanitised_faces: List[Face] = []
    uvs: List[UV] = []
    
    for face in self.faces:
      sanitised_face = SanitisedFace(face)
      sanitised_faces.append(sanitised_face)

      # Convert UVs - 4 per face
      for coords in face.texture_coords:
        uv = UV(coords, face.texture_index)
        uvs.append(uv)
        
    self.sanitised_faces = sanitised_faces
    self.uvs = uvs



  def __str__(self):
    return (
        f"Sanitised Model {self.name}\n"
        f"  ID: 0x{self.id:08X}\n"
        f"  Bones: {len(self.bones)}\n"
        f"  Vertices: {len(self.vertices)}\n"
        f"  Faces: {len(self.sanitised_faces)}\n"
        f"  UVs: {len(self.uvs)}\n"
    )