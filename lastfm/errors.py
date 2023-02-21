class LastFMException(Exception):
    """Base Last.FM Exception"""
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message


class InvalidParameters(LastFMException):
    """An invalid parameter has been passed"""
    pass


class OperationFailed(LastFMException):
    """A server side error has occurred"""
    pass


mapping = {
    6: InvalidParameters,
    8: OperationFailed
}
