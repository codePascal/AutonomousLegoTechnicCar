"""Drive control interface."""

from typing import Protocol


class DrivePort(Protocol):
    """Control longitudinal vehicle movement."""

    def drive(self, speed: float) -> None:
        """Drive at desired speed."""

    def stop(self) -> None:
        """Stop the drive and release its resources."""
