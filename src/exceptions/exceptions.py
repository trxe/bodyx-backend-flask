
class NotFoundError(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "Not found"
        super(NotFoundError, self).__init__(msg)
