
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


class AuthenticationError(Exception):
    def __init__(self):
        super(AuthenticationError, self).__init__("Could not verify username or password")


class InvalidTokenError(Exception):
    def __init__(self, missing=False):
        super(InvalidTokenError, self).__init__(f"Token is {'missing' if missing else 'invalid'}")


class NoAccessError(Exception):
    def __init__(self):
        super(NoAccessError, self).__init__("Insufficient access privileges")
