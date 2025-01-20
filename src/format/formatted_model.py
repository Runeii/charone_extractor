from dataclasses import dataclass
from typing import List
from ..parse.model.__parser import ModelParser
from ..parse.model.tim import TIM
from ..parse.model.bone import Bone
from ..parse.model.face import Face
from ..parse.model.vertex import Vertex
from ..parse.model.texture_animation import TextureAnimation
from ..parse.model.unknown_data_object import UnknownDataObject
from ..parse.model.animations.__parser import AnimationsParser

from .formatted_bone import FormattedBone
from .formatted_face import FormattedFace
from .formatted_vertex import FormattedVertex
from .animations.formatted_animation import FormattedAnimation

from .bone_indices import BoneIndices
from .uv import UV

@dataclass(init=False)
class FormattedModel:
  name: str
  textures: List[TIM]

  bones: List[FormattedBone]
  faces: List[FormattedFace]
  vertices: List[FormattedVertex]

  texture_animations: List[TextureAnimation]
  unknown_data_objects: List[UnknownDataObject]

  def __init__(self, model: ModelParser):
    self.name = model.header.model_name
    self.textures = model.textures

    self.bones = self.sanitise_bones(bones=model.model_data.bones)
    self.vertices = self.sanitise_vertices(vertices=model.model_data.vertices)
    self.faces = self.sanitise_faces(faces=model.model_data.faces)

    self.texture_animations = model.model_data.texture_animations
    self.unknown_data_objects = model.model_data.unknown_data_objects

    self.uvs = self.construct_uvs(faces=model.model_data.faces)

    self.bone_indices = BoneIndices(
      skin_objects=model.model_data.skin_objects,
      vertex_count=len(model.model_data.vertices)
    )

    self.animations = self.sanitise_animations(
      animations=model.model_data.animations,
      bones=self.bones
    )


  def sanitise_bones(self, bones: List[Bone]) -> List[FormattedBone]:
    return list(map(lambda bone : FormattedBone(bone), bones))

  def sanitise_vertices(self, vertices: List[Vertex]) -> List[FormattedVertex]:
    return list(map(lambda vertex : FormattedVertex(vertex), vertices))

  def sanitise_faces(self, faces: List[Face]) -> List[FormattedFace]:
    return list(map(lambda face : FormattedFace(face), faces))

  def construct_uvs(self, faces: List[Face]) -> List[UV]:
    flattened_uvs: List[UV] = []
    for face in faces:
      for coords in face.texture_coords:
        flattened_uvs.append(UV(coords, face.texture_index))
    return flattened_uvs

  def sanitise_animations(self, animations: AnimationsParser, bones: List[FormattedBone]) -> List[FormattedAnimation]:
    return list(map(lambda animation : FormattedAnimation(animation, bones), animations.animations))


  def __repr__(self) -> str:
    return f"Model: {self.name}\n"