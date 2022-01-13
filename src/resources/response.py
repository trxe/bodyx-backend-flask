class Response:
    def __init__(self, msg="", error="", data=None):
        self.msg = msg
        self.error = error
        self.data = data

    def to_json(self):
        return self.__dict__


def error_json(e: Exception) -> dict:
    return Response(error=str(e)).to_json()


def success_json(msg: str, data) -> dict:
    return Response(msg=msg, data=data).to_json()
