from typing import List, Optional, Sequence, Mapping, TypedDict

class BoneData(TypedDict):
    name: str
    parent: Optional[int]
    length: float
    transform: Mapping[str, Sequence[float]]
    child_count: int
    chain_length: int
    head: List[float]
    tail: List[float]
    roll: float 