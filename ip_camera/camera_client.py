from cv2 import cv2

from ip_camera.camera import Camera
from ip_camera.reconnecting_camera import ReconnectingCamera

if __name__ == '__main__':
    # test_url = 'http://131.95.3.162/mjpg/video.mjpg?timestamp=1635273492297'
    test_url = 'https://www.rmp-streaming.com/media/big-buck-bunny-360p.mp4'
    # test_url = 'http://185.97.122.128/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER'
    # test_url = 'http://localhost:8080/hls/stream.m3u8'

    for frame in ReconnectingCamera(Camera(test_url)):
        try:
            cv2.waitKey(150)
            cv2.imshow('sample', frame)
        except Exception as e:
            print(e)

