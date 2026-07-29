#!/usr/bin/env python
"""Pi-Camera Interface

Module implements a wrapper for a camera connected to Raspberry Pi via MIPI
CSI camera port.
"""

import time

import numpy as np
from picamera2 import Picamera2


class Camera:
    def __init__(self, size=(640, 480), fps=30):
        self.cam = Picamera2()

        cfg = self.cam.create_video_configuration(
            main={"size": size, "format": "RGB888"}, controls={"FrameRate": fps}
        )
        self.cam.configure(cfg)

    def setup(self) -> None:
        self.cam.start()

    def close(self) -> None:
        self.cam.stop()

    def read(self) -> tuple[float, np.ndarray]:
        frame = self.cam.capture_array()
        ts = time.time()
        return ts, frame


if __name__ == "__main__":
    from pathlib import Path

    from PIL import Image

    out = Path(__file__).parent.parent.parent.joinpath("out")
    out.mkdir(parents=True, exist_ok=True)

    cam = Camera(size=(640, 480), fps=30)
    cam.setup()
    time.sleep(0.5)

    # Capture image and save it
    _, image = cam.read()
    filename = out.joinpath("camera_test.jpg")
    Image.fromarray(image).save(filename)

    # Estimate frame-rate
    num_frames = 10
    t0 = time.time()
    for _ in range(num_frames):
        _ = cam.read()
    t1 = time.time()
    fps = num_frames / (t1 - t0)
    print(f"Estimated FPS: {fps:.2f}")

    cam.close()
