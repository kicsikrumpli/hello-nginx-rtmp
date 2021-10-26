class CameraException(BaseException):
    def __init__(self):
        super().__init__()


class CameraDisconnectedException(CameraException):
    def __init__(self):
        super().__init__()
