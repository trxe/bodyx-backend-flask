
class NotFoundError(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "Not found"
        super(NotFoundError, self).__init__(msg)


class MissingArgumentError(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "Missing argument"
        super(InvalidIdError, self).__init__(msg)


class InvalidIdError(Exception):
    def __init__(self, invalid_id=None):
        if not invalid_id:
            invalid_id = "Unknown ObjectId"
        super(InvalidIdError, self).__init__(f"{invalid_id} is an invalid ObjectId")
