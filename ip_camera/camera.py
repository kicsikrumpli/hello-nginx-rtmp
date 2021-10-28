import threading
import time
from contextlib import contextmanager
from functools import partial
from typing import Optional

import numpy as np
from cv2 import cv2
from cv2.cv2 import VideoCapture
from imutils.video import FPS

from ip_camera.camera_exception import CameraDisconnectedException


class Camera:
    def __init__(self,
                 source: str,
                 timeout_s=5):
        self.source = source
        self.video_capture: Optional[VideoCapture] = None
        self.capture_thread: Optional[threading.Thread] = None
        self.buffer: Optional[np.ndarray] = None
        self.lock = threading.Lock()
        self.timeout_s = timeout_s
        self.started = threading.Event()

    def __enter__(self):
        self.connect()
        self.start_capture()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

        if exc_type:
            print(exc_type, exc_val)
            return False

        return True

    def connect(self):
        self.started.clear()
        self.video_capture = VideoCapture(self.source)
        if self.video_capture is None:
            raise CameraDisconnectedException()
        if not self.video_capture.isOpened():
            raise CameraDisconnectedException()
        self.video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 10)

    @property
    def fps(self):
        try:
            current_frame = self.video_capture.get(cv2.CAP_PROP_POS_FRAMES)
            current_time = self.video_capture.get(cv2.CAP_PROP_POS_MSEC)
            return current_frame / (current_time / 1000)
        except Exception:
            # this is unreliable
            return self.video_capture.get(cv2.CAP_PROP_FPS)

    def start_capture(self):
        self.capture_thread = threading.Thread(target=self._capture_thread, daemon=True)
        self.capture_thread.start()

    def _capture_thread(self):
        print(f'starting capture thread.')
        while True:
            grabbed = self.video_capture.grab()
            if grabbed:
                buffer: np.ndarray
                with self.lock:
                    _, buffer = self.video_capture.retrieve()
                    self.buffer = buffer.copy()
                self.started.set()
                # print(self.fps)
                time.sleep(1 / self.fps)
            else:
                print('stopping capture thread')
                break

    def sample(self) -> np.ndarray:
        if not self.is_capturing():
            raise CameraDisconnectedException()
        try:
            self.started.wait(self.timeout_s)
            with self.lock_with_timeout(self.lock, self.timeout_s):
                return self.buffer
        except TimeoutError:
            print('capture timeout')
            raise CameraDisconnectedException()

    @staticmethod
    @contextmanager
    def lock_with_timeout(lock, timeout=5):
        locked = lock.acquire(blocking=True, timeout=timeout)
        if not locked:
            raise TimeoutError
        yield locked
        lock.release()

    def disconnect(self):
        if self.video_capture:
            self.video_capture.release()

    def is_capturing(self):
        return self.capture_thread.is_alive()
