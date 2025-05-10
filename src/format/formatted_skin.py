from dataclasses import dataclass
from src.parse.model.skin_object import SkinObject

@dataclass(init=False)
class FormattedSkin:
    first_vertex_index: int
    vertex_count: int
    bone_id: int

    def __init__(self, skin: SkinObject):
        self.first_vertex_index = skin.first_vertex_index
        self.vertex_count = skin.vertex_count
        self.bone_id = skin.bone_id - 1  # Convert from 1-based to 0-based

    def __repr__(self) -> str:
        return f"Skin: vertex_range={self.first_vertex_index}-{self.first_vertex_index + self.vertex_count - 1}, bone={self.bone_id}" 