import logging


class HypixelException(Exception):
    def __init__(self, message="An unknown error has occurred in the bedwars_api module. Please contact support."):
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        super().__init__(message)
        logging.debug(f"HypixelException raised: {message}")


class APIException(HypixelException):
    def __init__(self, message="An unknown error has occurred while attempting to use the API. Please contact support."):
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        super().__init__(message)
        logging.debug(f"ApiException raised: {message}")


class PlayerNotFoundException(APIException):
    def __init__(self, message="Player was not found in the API. Please contact support."):
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        super().__init__(message)
        logging.debug(f"PlayerNotFoundException raised: {message}")


class TimeoutException(APIException):
    def __init__(self, message="The API request timed out. Please contact support."):
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        super().__init__(message)
        logging.debug(f"TimeoutException raised: {message}")


class TooManyRequestsException(APIException):
    def __init__(self, message="The API has been rate limited. Please try again later."):
        logging.debug(f"Class {self.__class__.__name__}: __init__ called")
        super().__init__(message)
        logging.debug(f"TooManyRequestsException raised: {message}")
