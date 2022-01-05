class Response:
    def __init__(self, msg="", error="", data=None):
        self.msg = msg
        self.error = error
        self.data = data

    def to_json(self):
        return self.__dict__
