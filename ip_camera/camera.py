import threading
import time
from functools import partial
from typing import Optional

import numpy as np
from cv2 import cv2
from cv2.cv2 import VideoCapture
from imutils.video import FPS

from ip_camera.camera_exception import CameraDisconnectedException


class Camera:
    def __init__(self, source: str):
        self.source = source
        self.video_capture: Optional[VideoCapture] = None
        self.is_capturing = threading.Event()
        self.capture_thread: Optional[threading.Thread] = None
        self.buffer: Optional[np.ndarray] = None
        self.fps_meter = FPS()
        self.lock = threading.Lock()
        self.frame_ready = threading.Event()

    def __enter__(self):
        self.connect()
        self.start_capture()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type, exc_val)
        self.disconnect()
        return True

    def connect(self):
        self.video_capture = VideoCapture(self.source)
        if self.video_capture is None:
            raise CameraDisconnectedException()
        if not self.video_capture.isOpened():
            raise CameraDisconnectedException()

    def get_fps(self):
        return self.video_capture.get(cv2.CAP_PROP_FPS)

    def start_capture(self):
        fps = self.get_fps()
        self.capture_thread = threading.Thread(target=partial(self._capture_thread, fps))
        self.capture_thread.start()
        self.fps_meter.start()

    def _capture_thread(self, fps):
        # self.is_capturing.set()
        while True:
            grabbed = self.video_capture.grab()
            if grabbed:
                buffer: np.ndarray
                with self.lock:
                    _, buffer = self.video_capture.retrieve()
                    self.buffer = buffer.copy()
                self.frame_ready.set()
                self.fps_meter.update()
                time.sleep(1 / fps)
            else:
                self.is_capturing.clear()
                self.frame_ready.set()
                self.fps_meter.stop()
                break

    def sample(self) -> np.ndarray:
        if self.is_capturing.isSet():
            self.frame_ready.wait()
            with self.lock:
                self.frame_ready.clear()
                return self.buffer
        else:
            raise CameraDisconnectedException()

    def disconnect(self):
        if self.video_capture:
            self.video_capture.release()
