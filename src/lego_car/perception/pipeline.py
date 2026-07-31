"""Perception pipeline for processing captured camera frames."""

from dataclasses import dataclass

from lego_car.domain.models.camera_frame import CameraFrame


@dataclass(frozen=True, slots=True)
class PerceptionResult:
    frame_sequence: int
    frame_timestamp_ns: int
    width: int
    height: int
    channels: int


class PerceptionPipeline:
    def process(self, frame: CameraFrame) -> PerceptionResult:
        if frame.image.size == 0:
            raise ValueError("Cannot process an empty camera frame.")

        if frame.image.ndim not in (2, 3):
            raise ValueError(f"Unsupported frame dimensions: {frame.image.shape}")

        return PerceptionResult(
            frame_sequence=frame.sequence,
            frame_timestamp_ns=frame.timestamp_ns,
            width=frame.width,
            height=frame.height,
            channels=frame.channels,
        )
