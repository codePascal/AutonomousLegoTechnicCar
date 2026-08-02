"""Stepper-motor-based vehicle drive adapter."""

import time

from adafruit_motor import stepper  # type: ignore[import-untyped]
from adafruit_motorkit import MotorKit  # type: ignore[import-untyped]


class StepperDriveAdapter:
    def __init__(self, mounting_direction: int) -> None:
        self._motor = MotorKit()

        self._forward_direction = stepper.FORWARD
        self._backward_direction = stepper.BACKWARD
        self._handle_mounting_direction(mounting_direction)

        self._step_style = stepper.DOUBLE
        self._step_interval = 0.01

    def drive(self, speed: float) -> None:
        if speed == 0.0:
            self.stop()
        else:
            if speed < 0.0:
                direction = self._backward_direction
            else:
                direction = self._forward_direction
            for _ in range(100):
                self._motor.stepper1.onestep(direction=direction, style=self._step_style)
                time.sleep(self._step_interval)

    def stop(self) -> None:
        self._motor.stepper1.release()

    def _handle_mounting_direction(self, mounting_direction: int) -> None:
        if mounting_direction == -1:
            self._forward_direction = stepper.BACKWARD
            self._backward_direction = stepper.FORWARD
        else:
            self._forward_direction = stepper.FORWARD
            self._backward_direction = stepper.BACKWARD
