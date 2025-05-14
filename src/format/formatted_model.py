from dataclasses import dataclass
from typing import List
from src.parse.model.__parser import ModelParser
from src.parse.model.tim import TIM
from src.parse.model.bone import Bone
from src.parse.model.face import Face
from src.parse.model.vertex import Vertex
from src.parse.model.texture_animation import TextureAnimation
from src.parse.model.unknown_data_object import UnknownDataObject
from src.parse.model.animations.__parser import AnimationsParser
from src.parse.model.skin_object import SkinObject

from .formatted_bone import FormattedBone
from .formatted_face import FormattedFace
from .formatted_vertex import FormattedVertex
from .formatted_skin import FormattedSkin
from .animations.formatted_animation import FormattedAnimation
from .formatted_rest_pose import FormattedRestPose
@dataclass(init=False)
class FormattedModel:
  name: str
  textures: List[TIM]

  skin_objects: List[FormattedSkin]
  texture_animations: List[TextureAnimation]
  unknown_data_objects: List[UnknownDataObject]

  bones: List[FormattedBone]
  faces: List[FormattedFace]
  vertices: List[FormattedVertex]

  rest_pose: FormattedRestPose

  def __init__(self, model: ModelParser):
    self.name = model.header.model_name.replace("x", "")
    self.textures = model.textures

    self.texture_animations = model.model_data.texture_animations
    self.unknown_data_objects = model.model_data.unknown_data_objects
    self.skin_objects = self.sanitise_skins(skins=model.model_data.skin_objects)

    self.bones = self.sanitise_bones(bones=model.model_data.bones)
    self.vertices = self.sanitise_vertices(vertices=model.model_data.vertices)
    self.faces = self.sanitise_faces(faces=model.model_data.faces)

    self.animations = self.sanitise_animations(
      animations=model.model_data.animations,
      bones=self.bones
    )

    self.rest_pose = FormattedRestPose(model.model_data.rest_animation)

  def sanitise_bones(self, bones: List[Bone]) -> List[FormattedBone]:
    return list(map(lambda bone : FormattedBone(bone), bones))

  def sanitise_vertices(self, vertices: List[Vertex]) -> List[FormattedVertex]:
    return list(map(lambda vertex : FormattedVertex(vertex), vertices))

  def sanitise_faces(self, faces: List[Face]) -> List[FormattedFace]:
    return list(map(lambda face : FormattedFace(face), faces))

  def sanitise_skins(self, skins: List[SkinObject]) -> List[FormattedSkin]:
    return list(map(lambda skin: FormattedSkin(skin), skins))

  def sanitise_animations(self, animations: AnimationsParser, bones: List[FormattedBone]) -> List[FormattedAnimation]:
    return list(map(lambda animation : FormattedAnimation(animation, bones), animations.animations))

  def __repr__(self) -> str:
    return f"Model: {self.name}\n"