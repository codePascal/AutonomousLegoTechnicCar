"""Application entry point for camera capture and perception processing."""

import logging
import time

from lego_car.infrastructure.camera.picamera2_adapter import Picamera2Adapter
from lego_car.perception.pipeline import PerceptionPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

LOGGER = logging.getLogger(__name__)


def main() -> None:
    camera = Picamera2Adapter(
        width=640,
        height=480,
    )
    pipeline = PerceptionPipeline()

    frame_count = 0
    started_ns = time.monotonic_ns()

    try:
        with camera:
            while True:
                frame = camera.capture_frame()
                result = pipeline.process(frame)

                frame_count += 1

                if frame_count % 30 == 0:
                    elapsed_seconds = (time.monotonic_ns() - started_ns) / 1_000_000_000

                    frames_per_second = frame_count / elapsed_seconds

                    LOGGER.info(
                        "frame=%d resolution=%dx%d channels=%d fps=%.1f",
                        result.frame_sequence,
                        result.width,
                        result.height,
                        result.channels,
                        frames_per_second,
                    )

    except KeyboardInterrupt:
        LOGGER.info("Camera processing stopped by user.")


if __name__ == "__main__":
    main()
