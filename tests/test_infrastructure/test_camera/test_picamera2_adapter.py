"""Tests for the Picamera2 camera adapter."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from lego_car.infrastructure.camera.picamera2_adapter import Picamera2Adapter

pytestmark = pytest.mark.hardware


@pytest.fixture
def picamera2_mock() -> Generator[MagicMock, None, None]:
    with patch("lego_car.infrastructure.camera.picamera2_adapter.Picamera2") as picamera2_class:
        camera = MagicMock()
        picamera2_class.return_value = camera
        yield camera


def test_rejects_invalid_width() -> None:
    with pytest.raises(ValueError, match="width"):
        Picamera2Adapter(width=0, height=480)


def test_rejects_invalid_height() -> None:
    with pytest.raises(ValueError, match="height"):
        Picamera2Adapter(width=640, height=0)


def test_capture_before_start_raises_error() -> None:
    adapter = Picamera2Adapter()

    with pytest.raises(RuntimeError, match="not been started"):
        adapter.capture_frame()


def test_start_configures_and_starts_camera(picamera2_mock: MagicMock) -> None:
    adapter = Picamera2Adapter(
        width=640,
        height=480,
        pixel_format="RGB888",
    )

    adapter.start()

    picamera2_mock.create_video_configuration.assert_called_once_with(
        main={
            "size": (640, 480),
            "format": "RGB888",
        },
        buffer_count=4,
    )
    picamera2_mock.configure.assert_called_once()
    picamera2_mock.start.assert_called_once_with()


def test_start_twice_raises_error(picamera2_mock: MagicMock) -> None:
    adapter = Picamera2Adapter()
    adapter.start()

    with pytest.raises(RuntimeError, match="already running"):
        adapter.start()


def test_capture_returns_frame_and_increments_sequence(picamera2_mock: MagicMock) -> None:
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    picamera2_mock.capture_array.return_value = image

    adapter = Picamera2Adapter()
    adapter.start()

    first_frame = adapter.capture_frame()
    second_frame = adapter.capture_frame()

    assert first_frame.image is image
    assert first_frame.sequence == 0
    assert first_frame.timestamp_ns > 0
    assert first_frame.width == 640
    assert first_frame.height == 480
    assert first_frame.channels == 3

    assert second_frame.sequence == 1
    assert second_frame.timestamp_ns >= first_frame.timestamp_ns

    assert picamera2_mock.capture_array.call_count == 2
    picamera2_mock.capture_array.assert_called_with("main")


def test_capture_rejects_unexpected_frame_type(picamera2_mock: MagicMock) -> None:
    picamera2_mock.capture_array.return_value = "not an array"

    adapter = Picamera2Adapter()
    adapter.start()

    with pytest.raises(RuntimeError, match="unexpected frame type"):
        adapter.capture_frame()


def test_capture_rejects_unexpected_dtype(picamera2_mock: MagicMock) -> None:
    picamera2_mock.capture_array.return_value = np.zeros(
        (480, 640, 3),
        dtype=np.float32,
    )

    adapter = Picamera2Adapter()
    adapter.start()

    with pytest.raises(RuntimeError, match="Expected uint8"):
        adapter.capture_frame()


def test_stop_stops_and_closes_camera(picamera2_mock: MagicMock) -> None:
    adapter = Picamera2Adapter()
    adapter.start()

    adapter.stop()

    picamera2_mock.stop.assert_called_once_with()
    picamera2_mock.close.assert_called_once_with()


def test_stop_can_be_called_twice(picamera2_mock: MagicMock) -> None:
    adapter = Picamera2Adapter()
    adapter.start()

    adapter.stop()
    adapter.stop()

    picamera2_mock.stop.assert_called_once_with()
    picamera2_mock.close.assert_called_once_with()
