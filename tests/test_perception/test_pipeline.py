import numpy as np
import pytest

from lego_car.domain.models.camera_frame import CameraFrame
from lego_car.perception.pipeline import PerceptionPipeline


def test_process_returns_frame_information() -> None:
    frame = CameraFrame(
        image=np.zeros((480, 640, 3), dtype=np.uint8),
        sequence=42,
        timestamp_ns=123_456,
    )

    result = PerceptionPipeline().process(frame)

    assert result.frame_sequence == 42
    assert result.frame_timestamp_ns == 123_456
    assert result.width == 640
    assert result.height == 480
    assert result.channels == 3


def test_process_rejects_empty_frame() -> None:
    frame = CameraFrame(
        image=np.array([], dtype=np.uint8),
        sequence=0,
        timestamp_ns=123_456,
    )

    with pytest.raises(ValueError, match="empty camera frame"):
        PerceptionPipeline().process(frame)
