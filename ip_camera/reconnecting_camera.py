import time
from typing import Generator

from ip_camera.camera import Camera
from ip_camera.camera_exception import CameraException


class ReconnectingCamera:
    def __init__(self,
                 camera: Camera,
                 reconnect_timeout_s: int = 5
                 ):
        self.camera = camera
        self.reconnect_timeout_s = reconnect_timeout_s

    def __iter__(self) -> Generator[object, None, None]:
        while True:
            yield from self.stream()
            print(f'reconnnecting in {self.reconnect_timeout_s}s.')
            time.sleep(self.reconnect_timeout_s)

    def stream(self):
        try:
            with self.camera as cam:
                while cam.is_capturing():
                    yield cam.sample()
        except CameraException as e:
            print(e)
        else:
            print('---')
