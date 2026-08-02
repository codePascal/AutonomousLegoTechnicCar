"""Manually exercise the steering stepper motor."""

import time

from lego_car.infrastructure.movement.stepper_drive_adapter import StepperDriveAdapter


def main() -> None:
    motor = StepperDriveAdapter(mounting_direction=-1)
    motor.drive(speed=1)
    motor.drive(speed=-1)
    motor.drive(speed=0)


if __name__ == "__main__":
    main()