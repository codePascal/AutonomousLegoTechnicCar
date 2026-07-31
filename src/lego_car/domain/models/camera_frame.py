"""Domain model representing a captured camera frame."""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

ImageArray = npt.NDArray[np.uint8]


@dataclass(frozen=True, slots=True)
class CameraFrame:
    image: ImageArray
    sequence: int
    timestamp_ns: int

    @property
    def width(self) -> int:
        return int(self.image.shape[1])

    @property
    def height(self) -> int:
        return int(self.image.shape[0])

    @property
    def channels(self) -> int:
        if self.image.ndim == 2:
            return 1
        return int(self.image.shape[2])
