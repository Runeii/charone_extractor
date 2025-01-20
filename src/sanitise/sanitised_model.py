from dataclasses import dataclass, field
from typing import List
from ..parse.model.__parser import ParsedModel
from ..parse.model.tim import TIM
from ..parse.model.bone import Bone
from ..parse.model.texture_animation import TextureAnimation
from ..parse.model.face import Face
from ..parse.model.vertex import Vertex
from ..parse.model.skin_object import SkinObject
from ..parse.model.unknown_data_object import UnknownDataObject

from .sanitised_face import SanitisedFace
from .uv import UV
from .sanitised_bone import SanitisedBone
from .sanitised_vertex import SanitisedVertex
from .bone_indices import BoneIndices

from ..parse.m import Animation as ParsedAnimation
from .animation.animation import Animation

@dataclass
class SanitisedModel:
  model: ParsedModel

  id: int = field(init=False)
  name: str = field(init=False)
  tim: TIM = field(init=False)

  bones: List[SanitisedBone] = field(init=False)
  faces: List[SanitisedFace] = field(init=False)
  uvs: List[UV] = field(init=False)

  texture_animations: List[TextureAnimation] = field(init=False)
  vertices: List[Vertex] = field(init=False)
  skin_objects: List[SkinObject] = field(init=False)
  unknown_data_objects: List[UnknownDataObject] = field(init=False)

  animations: List[Animation] = field(init=False)


  def __post_init__(self):
    self.id = self.model.id
    self.name = self.model.name

    self.tim = self.model.tim

    self.bones = self.sanitise_bones(self.model.model_data.bones)
    self.vertices = self.sanitise_vertices(self.model.model_data.vertices)
    self.faces = self.sanitise_faces(self.model.model_data.faces)
    self.uvs = self.construct_uvs(self.model.model_data.faces)
    self.bone_indices = BoneIndices(self.vertices, self.model.model_data.skin_objects)

    self.texture_animations = self.model.model_data.texture_animations
    self.unknown_data_objects = self.model.model_data.unknown_data_objects

    self.animations = self.sanitise_animations(self.model.model_data.animations.animations, self.bones)
  

  @staticmethod
  def sanitise_bones(bones: List[Bone]) -> List[SanitisedBone]:
    return list(map(lambda bone : SanitisedBone(bone), bones))

  @staticmethod
  def sanitise_vertices(vertices: List[Vertex]) -> List[SanitisedVertex]:
    return list(map(lambda vertex : SanitisedVertex(vertex), vertices))

  @staticmethod
  def sanitise_faces(faces: List[Face]) -> List[SanitisedFace]:
    return list(map(lambda face : SanitisedFace(face), faces))

  @staticmethod
  def sanitise_animations(animations: List[ParsedAnimation], bones: List[SanitisedBone]) -> List[Animation]:
    return list(map(lambda animation : Animation(animation, bones), animations))

  @staticmethod
  def construct_uvs(faces: List[Face]) -> List[SanitisedFace]:
    flattened_uvs = []
    for face in faces:
      for coords in face.texture_coords:
        flattened_uvs.append(UV(coords, face.texture_index))
    return flattened_uvs

  def __str__(self):
    return (
        f"Sanitised Model {self.name}\n"
        f"  ID: 0x{self.id:08X}\n"
        f"  Bones: {len(self.bones)}\n"
        f"  Vertices: {len(self.vertices)}\n"
        f"  Faces: {len(self.faces)}\n"
        f"  UVs: {len(self.uvs)}\n"
    )