"""Temporary bone name mappings for FF8 character models.
This module will be replaced with a different bone identification system in the future.
"""

from typing import Dict, Optional, Protocol, List, Union

BONE_NAMES=\
  ["root","upperbody","lowerbody","neck","collar0","collar1","collar2","collar3","collar4",\
  "collar5","breast_L","breast_R","cape0","cape1","cape2","cape3","cape4","cape5",\
  "head","hair0","hair1","hair2","hair3","hair4","hair5","shoulder_L","shoulder_R",\
  "arm_L","arm_R","forearm_L","forearm_R","hand_L","hand_R","dress0","dress1","dress2",\
  "dress3","dress4","dress5","dress6","hip_L","hip_R","belt0","belt1","belt2",\
  "belt3","belt4","belt5","thigh_L","thigh_R","tibia_L","tibia_R","foot_L","foot_R"]

# Common bone sequence rows used across characters
FIRST_ROW = [0, 1, 2, 4, "N", "N", "N", "N", "N"]
SECOND_ROW = ["N", 3, 5, "N", "N", "N", "N", "N", "N"]
THIRD_ROW = [9, "N", "N", "N", "N", "N", "N", 8, 10]
FIFTH_ROW = ["N", "N", "N", "N", 6, 7, "N", "N", "N"]
SIXTH_ROW = ["N", "N", "N", 11, 12, 15, 16, 19, 20]

# Character-specific bone sequences
CHARACTER_BONE_SEQUENCES: Dict[str, List[Union[int, str]]] = {
    # Rinoa + Soldier/Spacesuit Rinoa
    "d022": FIRST_ROW + ["N", 3, 5, "N", "N", "N", 6, 12, 18, 10, 16, 22, 27, 29, 30, 31, 9, 11, 15, 17, 21, 23, 26, 28, "N", "N", "N", "N", "N", "N", "N", 7, 8, "N", "N", "N", "N", "N", "N", 13, 14, 19, 20, 24, 25],
    "d023": FIRST_ROW + ["N", 3, 5, "N", "N", "N", 6, 12, 18, 10, 16, 22, 27, 29, 30, 31, 9, 11, 15, 17, 21, 23, 26, 28, "N", "N", "N", "N", "N", "N", "N", 7, 8, "N", "N", "N", "N", "N", "N", 13, 14, 19, 20, 24, 25],
    "d024": FIRST_ROW + ["N", 3, 5, "N", "N", "N", 6, 12, 18, 10, 16, 22, 27, 29, 30, 31, 9, 11, 15, 17, 21, 23, 26, 28, "N", "N", "N", "N", "N", "N", "N", 7, 8, "N", "N", "N", "N", "N", "N", 13, 14, 19, 20, 24, 25],
    "d025": FIRST_ROW + ["N", 3, 5, "N", "N", "N", 6, 12, 18, 10, 16, 22, 27, 29, 30, 31, 9, 11, 15, 17, 21, 23, 26, 28, "N", "N", "N", "N", "N", "N", "N", 7, 8, "N", "N", "N", "N", "N", "N", 13, 14, 19, 20, 24, 25],
    "d026": FIRST_ROW + ["N", 3, 5, "N", "N", "N", 6, 12, 18, 10, 16, 22, 27, 29, 30, 31, 9, 11, 15, 17, 21, 23, 26, 28, "N", "N", "N", "N", "N", "N", "N", 7, 8, "N", "N", "N", "N", "N", "N", 13, 14, 19, 20, 24, 25],
    "d051": FIRST_ROW + ["N", 3, 5, "N", "N", "N", 6, 12, 18, 10, 16, 22, 27, 29, 30, 31, 9, 11, 15, 17, 21, 23, 26, 28, "N", "N", "N", "N", "N", "N", "N", 7, 8, "N", "N", "N", "N", "N", "N", 13, 14, 19, 20, 24, 25],
    "d075": FIRST_ROW + ["N", 3, 5, "N", "N", "N", 6, 12, 18, 10, 16, 22, 27, 29, 30, 31, 9, 11, 15, 17, 21, 23, 26, 28, "N", "N", "N", "N", "N", "N", "N", 7, 8, "N", "N", "N", "N", "N", "N", 13, 14, 19, 20, 24, 25],
    "d067": FIRST_ROW + ["N", 3, 5, "N", "N", "N", 6, 12, 18, 10, 16, 22, 27, 29, 30, 31, 9, 11, 15, 17, 21, 23, 26, 28, "N", "N", "N", "N", "N", "N", "N", 7, 8, "N", "N", "N", "N", "N", "N", 13, 14, 19, 20, 24, 25],
    "d061": FIRST_ROW + ["N", 3, 5, "N", "N", "N", 6, 12, 18, 10, 16, 22, 27, 29, 30, 31, 9, 11, 15, 17, 21, 23, 26, 28, "N", "N", "N", "N", "N", "N", "N", 7, 8, "N", "N", "N", "N", "N", "N", 13, 14, 19, 20, 24, 25],

    # Squall + Spacesuit Squall
    "d000": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d001": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d002": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d003": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d004": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d005": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d006": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d007": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d049": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d052": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d053": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,
    "d060": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, 23, 24, "N"] + FIFTH_ROW + SIXTH_ROW,

    # Selphie + Soldier Selphie
    "d027": FIRST_ROW + SECOND_ROW + [9, 14, 19, "N", "N", "N", "N", 8, 10, 13, 15, 18, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 16, 17, 21, 22],
    "d028": FIRST_ROW + SECOND_ROW + [9, 14, 19, "N", "N", "N", "N", 8, 10, 13, 15, 18, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 16, 17, 21, 22],
    "d029": FIRST_ROW + SECOND_ROW + [9, 14, 19, "N", "N", "N", "N", 8, 10, 13, 15, 18, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 16, 17, 21, 22],
    "d030": FIRST_ROW + SECOND_ROW + [9, 14, 19, "N", "N", "N", "N", 8, 10, 13, 15, 18, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 16, 17, 21, 22],
    "d066": FIRST_ROW + SECOND_ROW + [9, 14, 19, "N", "N", "N", "N", 8, 10, 13, 15, 18, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 16, 17, 21, 22],

    # Zell + Kids + Soldier Zell
    "d009": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,
    "d010": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,
    "d011": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,
    "d012": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,
    "d014": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,
    "d054": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,
    "d055": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,
    "d056": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,
    "d057": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,
    "d059": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,
    "d069": FIRST_ROW + SECOND_ROW + THIRD_ROW + [13, 14, 17, 18, 21, 22, "N", "N", "N"] + FIFTH_ROW + SIXTH_ROW,

    # Irvine + Soldier
    "d015": FIRST_ROW + ["N", 3, 6, 5, 11, "N", "N", "N", "N", 10, 18, 25, 32, "N", "N", "N", 9, 14, 17, 21, 24, 28, 31, 33, 19, "N", 26, 20, "N", 27, "N", 7, 8, 12, 13, "N", "N", "N", "N", 15, 16, 22, 23, 29, 30],
    "d016": FIRST_ROW + ["N", 3, 6, 5, 11, "N", "N", "N", "N", 10, 18, 25, 32, "N", "N", "N", 9, 14, 17, 21, 24, 28, 31, 33, 19, "N", 26, 20, "N", 27, "N", 7, 8, 12, 13, "N", "N", "N", "N", 15, 16, 22, 23, 29, 30],
    "d017": FIRST_ROW + ["N", 3, 6, 5, 11, "N", "N", "N", "N", 10, 18, 25, 32, "N", "N", "N", 9, 14, 17, 21, 24, 28, 31, 33, 19, "N", 26, 20, "N", 27, "N", 7, 8, 12, 13, "N", "N", "N", "N", 15, 16, 22, 23, 29, 30],
    "d070": FIRST_ROW + ["N", 3, 6, 5, 11, "N", "N", "N", "N", 10, 18, 25, 32, "N", "N", "N", 9, 14, 17, 21, 24, 28, 31, 33, 19, "N", 26, 20, "N", 27, "N", 7, 8, 12, 13, "N", "N", "N", "N", 15, 16, 22, 23, 29, 30],

    # Quistis + Soldier Quistis
    "d018": FIRST_ROW + SECOND_ROW + [9, 14, 20, 15, 21, "N", "N", 8, 10, 13, 16, 19, 22, 25, 26, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 17, 18, 23, 24],
    "d019": FIRST_ROW + SECOND_ROW + [9, 14, 20, 15, 21, "N", "N", 8, 10, 13, 16, 19, 22, 25, 26, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 17, 18, 23, 24],
    "d020": FIRST_ROW + SECOND_ROW + [9, 14, 20, 15, 21, "N", "N", 8, 10, 13, 16, 19, 22, 25, 26, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 17, 18, 23, 24],
    "d021": FIRST_ROW + SECOND_ROW + [9, 14, 20, 15, 21, "N", "N", 8, 10, 13, 16, 19, 22, 25, 26, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 17, 18, 23, 24],
    "d050": FIRST_ROW + SECOND_ROW + [9, 14, 20, 15, 21, "N", "N", 8, 10, 13, 16, 19, 22, 25, 26, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 17, 18, 23, 24],
    "d068": FIRST_ROW + SECOND_ROW + [9, 14, 20, 15, 21, "N", "N", 8, 10, 13, 16, 19, 22, 25, 26, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 17, 18, 23, 24],

    # Edea
    "d040": FIRST_ROW + ["N", 3, 5, 9, 12, "N", "N", "N", "N", 10, "N", "N", "N", "N", "N", "N", 8, 11, 15, 16, 19, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 13, 14, 17, 18, 21, 22],
    "d041": FIRST_ROW + ["N", 3, 5, 9, 12, "N", "N", "N", "N", 10, "N", "N", "N", "N", "N", "N", 8, 11, 15, 16, 19, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 13, 14, 17, 18, 21, 22],
    "d042": FIRST_ROW + ["N", 3, 5, 9, 12, "N", "N", "N", "N", 10, "N", "N", "N", "N", "N", "N", 8, 11, 15, 16, 19, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 13, 14, 17, 18, 21, 22],
    "d035": FIRST_ROW + ["N", 3, 5, 9, 12, "N", "N", "N", "N", 10, "N", "N", "N", "N", "N", "N", 8, 11, 15, 16, 19, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 13, 14, 17, 18, 21, 22],
    "d074": FIRST_ROW + ["N", 3, 5, 9, 12, "N", "N", "N", "N", 10, "N", "N", "N", "N", "N", "N", 8, 11, 15, 16, 19, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 13, 14, 17, 18, 21, 22],

    # Kid Quistis
    "d058": FIRST_ROW + SECOND_ROW + [9, 14, "N", "N", "N", "N", 19, 8, 10, 13, 15, 18, 20, 23, 24, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 16, 17, 21, 22],

    # Kiros + Spacesuit Kiros
    "d045": FIRST_ROW + ["N", 3, 5, 28, 32, 34, 27, 31, 33, 9, 14, 19, 26, 30, 21, 20, 8, 10, 13, 15, 18, 22, 25, 29, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 16, 17, 23, 24],
    "d046": FIRST_ROW + ["N", 3, 5, 28, 32, 34, 27, 31, 33, 9, 14, 19, 26, 30, 21, 20, 8, 10, 13, 15, 18, 22, 25, 29, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 16, 17, 23, 24],
    "d072": FIRST_ROW + ["N", 3, 5, 28, 32, 34, 27, 31, 33, 9, 14, 19, 26, 30, 21, 20, 8, 10, 13, 15, 18, 22, 25, 29, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 16, 17, 23, 24],
    "d063": FIRST_ROW + ["N", 3, 5, 28, 32, 34, 27, 31, 33, 9, 14, 19, 26, 30, 21, 20, 8, 10, 13, 15, 18, 22, 25, 29, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 11, 12, 16, 17, 23, 24],

    # Ward + Spacesuit Ward
    "d047": FIRST_ROW + ["N", 3, 5, 12, 14, "N", "N", "N", "N", 9, "N", "N", "N", "N", "N", "N", 8, 10, 15, 16, 25, 26, 29, 30, "N", "N", "N", "N", "N", "N", "N", 6, 7, 18, 19, 20, 22, 23, 24, 11, 13, 17, 21, 27, 28],
    "d048": FIRST_ROW + ["N", 3, 5, 12, 14, "N", "N", "N", "N", 9, "N", "N", "N", "N", "N", "N", 8, 10, 15, 16, 25, 26, 29, 30, "N", "N", "N", "N", "N", "N", "N", 6, 7, 18, 19, 20, 22, 23, 24, 11, 13, 17, 21, 27, 28],
    "d073": FIRST_ROW + ["N", 3, 5, 12, 14, "N", "N", "N", "N", 9, "N", "N", "N", "N", "N", "N", 8, 10, 15, 16, 25, 26, 29, 30, "N", "N", "N", "N", "N", "N", "N", 6, 7, 18, 19, 20, 22, 23, 24, 11, 13, 17, 21, 27, 28],
    "d064": FIRST_ROW + ["N", 3, 5, 12, 14, "N", "N", "N", "N", 9, "N", "N", "N", "N", "N", "N", 8, 10, 15, 16, 25, 26, 29, 30, "N", "N", "N", "N", "N", "N", "N", 6, 7, 18, 19, 20, 22, 23, 24, 11, 13, 17, 21, 27, 28],

    # Seifer
    "d032": [0, 1, 2, 6, 8, 20, 5, 17, "N", "N", 4, 7, 3, 11, "N", "N", "N", "N", 18, "N", "N", "N", "N", "N", "N", 16, 19, 27, 28, 35, 36, 39, 40, 23, 31, 32, 25, 33, 34, "N", 9, 10, 12, 14, 13, 24, 15, 26, 21, 22, 29, 30, 37, 38],
    "d033": [0, 1, 2, 6, 8, 20, 5, 17, "N", "N", 4, 7, 3, 11, "N", "N", "N", "N", 18, "N", "N", "N", "N", "N", "N", 16, 19, 27, 28, 35, 36, 39, 40, 23, 31, 32, 25, 33, 34, "N", 9, 10, 12, 14, 13, 24, 15, 26, 21, 22, 29, 30, 37, 38],
    "d034": [0, 1, 2, 6, 8, 20, 5, 17, "N", "N", 4, 7, 3, 11, "N", "N", "N", "N", 18, "N", "N", "N", "N", "N", "N", 16, 19, 27, 28, 35, 36, 39, 40, 23, 31, 32, 25, 33, 34, "N", 9, 10, 12, 14, 13, 24, 15, 26, 21, 22, 29, 30, 37, 38],
    "d035": [0, 1, 2, 6, 8, 20, 5, 17, "N", "N", 4, 7, 3, 11, "N", "N", "N", "N", 18, "N", "N", "N", "N", "N", "N", 16, 19, 27, 28, 35, 36, 39, 40, 23, 31, 32, 25, 33, 34, "N", 9, 10, 12, 14, 13, 24, 15, 26, 21, 22, 29, 30, 37, 38],
    "d036": [0, 1, 2, 6, 8, 20, 5, 17, "N", "N", 4, 7, 3, 11, "N", "N", "N", "N", 18, "N", "N", "N", "N", "N", "N", 16, 19, 27, 28, 35, 36, 39, 40, 23, 31, 32, 25, 33, 34, "N", 9, 10, 12, 14, 13, 24, 15, 26, 21, 22, 29, 30, 37, 38],
    "d037": [0, 1, 2, 6, 8, 20, 5, 17, "N", "N", 4, 7, 3, 11, "N", "N", "N", "N", 18, "N", "N", "N", "N", "N", "N", 16, 19, 27, 28, 35, 36, 39, 40, 23, 31, 32, 25, 33, 34, "N", 9, 10, 12, 14, 13, 24, 15, 26, 21, 22, 29, 30, 37, 38],
    "d065": [0, 1, 2, 6, 8, 20, 5, 17, "N", "N", 4, 7, 3, 11, "N", "N", "N", "N", 18, "N", "N", "N", "N", "N", "N", 16, 19, 27, 28, 35, 36, 39, 40, 23, 31, 32, 25, 33, 34, "N", 9, 10, 12, 14, 13, 24, 15, 26, 21, 22, 29, 30, 37, 38],

    # Laguna + Spacesuit Laguna
    "d043": [0, 1, 2, 4, 12, 19, 9, 16, "N", "N", 3, 5, "N", "N", "N", "N", "N", "N", 10, 17, "N", "N", "N", "N", 23, 8, 11, 15, 18, 22, 24, 27, 28, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 13, 14, 20, 21, 25, 26],
    "d044": [0, 1, 2, 4, 12, 19, 9, 16, "N", "N", 3, 5, "N", "N", "N", "N", "N", "N", 10, 17, "N", "N", "N", "N", 23, 8, 11, 15, 18, 22, 24, 27, 28, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 13, 14, 20, 21, 25, 26],
    "d071": [0, 1, 2, 4, 12, 19, 9, 16, "N", "N", 3, 5, "N", "N", "N", "N", "N", "N", 10, 17, "N", "N", "N", "N", 23, 8, 11, 15, 18, 22, 24, 27, 28, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 13, 14, 20, 21, 25, 26],
    "d062": [0, 1, 2, 4, 12, 19, 9, 16, "N", "N", 3, 5, "N", "N", "N", "N", "N", "N", 10, 17, "N", "N", "N", "N", 23, 8, 11, 15, 18, 22, 24, 27, 28, "N", "N", "N"] + FIFTH_ROW + ["N", "N", "N", 13, 14, 20, 21, 25, 26]
}


def get_bone_name(index: int, model_name: str) -> str:
    """Get bone name for a given index.
    This is a temporary function that will be removed in the future.
    
    Args:
        index: Bone index
        character_type: Optional character type for specific bone mappings
        
    Returns:
        Bone name
    """
    if model_name and model_name in CHARACTER_BONE_SEQUENCES:
        print("Got sequence for: ", model_name)
        sequence = CHARACTER_BONE_SEQUENCES[model_name]
        # Find the index of the VALUE of index in the sequence
        bone_index = sequence.index(index)
        print("Bone index: ", bone_index)
        return BONE_NAMES[bone_index]
      
    print("Unknown bone: ", model_name, index)
    return "N"