from cv2 import cv2

from ip_camera.camera import Camera
from ip_camera.camera_exception import CameraException

if __name__ == '__main__':
    # test_url = 'http://131.95.3.162/mjpg/video.mjpg?timestamp=1635273492297'
    test_url = 'https://www.rmp-streaming.com/media/big-buck-bunny-360p.mp4'

    with Camera(source=test_url) as cam:
        cam: Camera
        while True:
            try:
                cv2.imshow('sample', cam.sample())
                cv2.waitKey(25)
            except CameraException as e:
                print(e)
                print(cam.fps_meter.fps())
                print(cam.fps_meter.elapsed())
                break

    print('--- done ---')

