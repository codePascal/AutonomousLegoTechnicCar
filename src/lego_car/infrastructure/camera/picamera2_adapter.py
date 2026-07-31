"""Picamera2-based camera adapter for Raspberry Pi hardware."""

import time
from typing import Any

import numpy as np
from picamera2 import Picamera2

from lego_car.domain.models.camera_frame import CameraFrame
from lego_car.domain.ports.camera import CameraPort


class Picamera2Adapter(CameraPort):
    def __init__(self, width: int = 640, height: int = 480, pixel_format: str = "RGB888") -> None:
        if width <= 0:
            raise ValueError("Camera width must be greater than zero.")
        if height <= 0:
            raise ValueError("Camera height must be greater than zero.")

        self._width = width
        self._height = height
        self._pixel_format = pixel_format

        self._camera: Picamera2 | None = None
        self._sequence = 0

    def start(self) -> None:
        if self._camera is not None:
            raise RuntimeError("Camera is already running.")

        camera = Picamera2()

        configuration = camera.create_video_configuration(
            main={
                "size": (self._width, self._height),
                "format": self._pixel_format,
            },
            buffer_count=4,
        )

        camera.configure(configuration)
        camera.start()

        self._camera = camera
        self._sequence = 0

    def capture_frame(self) -> CameraFrame:
        camera = self._require_camera()

        image: Any = camera.capture_array("main")

        if not isinstance(image, np.ndarray):
            raise RuntimeError(f"Picamera2 returned an unexpected frame type: {type(image)!r}")

        if image.dtype != np.uint8:
            raise RuntimeError(f"Expected uint8 camera data, received {image.dtype}.")

        frame = CameraFrame(
            image=image,
            sequence=self._sequence,
            timestamp_ns=time.monotonic_ns(),
        )

        self._sequence += 1
        return frame

    def stop(self) -> None:
        if self._camera is None:
            return

        try:
            self._camera.stop()
        finally:
            self._camera.close()
            self._camera = None

    def _require_camera(self) -> Picamera2:
        if self._camera is None:
            raise RuntimeError("Camera has not been started.")

        return self._camera
