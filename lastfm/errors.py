class LastFMException(Exception):
    """Base Lastf.FM Exception"""
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message


class InvalidParamaters(LastFMException):
    """An invalid paramater has been passed"""
    pass


class OperationFailed(LastFMException):
    """A server side error has occurred"""
    pass


mapping = {
    6: InvalidParamaters,
    8: OperationFailed
}
