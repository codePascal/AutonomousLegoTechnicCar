"""Hardware-independent interface for camera implementations."""

from abc import ABC, abstractmethod

from lego_car.domain.models.camera_frame import CameraFrame


class CameraPort(ABC):
    @abstractmethod
    def start(self) -> None:
        """Initialize the camera and begin frame acquisition."""

    @abstractmethod
    def capture_frame(self) -> CameraFrame:
        """Capture and return the next available camera frame."""

    @abstractmethod
    def stop(self) -> None:
        """Stop frame acquisition and release camera resources."""

    def __enter__(self) -> "CameraPort":
        self.start()
        return self

    def __exit__(self, exception_type: object, exception: object, traceback: object) -> None:
        self.stop()
