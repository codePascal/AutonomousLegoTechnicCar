"""Frame preprocessing for the perception pipeline."""

from dataclasses import dataclass

from numpy.typing import NDArray


@dataclass(frozen=True)
class PreprocessingConfig:
    width: int
    height: int
    grayscale: bool = False


class FramePreprocessor:
    def __init__(self, config: PreprocessingConfig) -> None:
        self._config = config

    def process(self, frame: NDArray) -> NDArray:
        ...