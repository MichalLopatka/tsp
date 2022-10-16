from dataclasses import dataclass
import numpy as np

@dataclass()
class City:
    city_id: int
    x: int
    y: int


@dataclass()
class Cities:
    cities: list[City]

@dataclass()
class Distance:
    matrix: np.array