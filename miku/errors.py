from typing import Any, Dict, List, Type, Union

__all__ = (
    'HTTPException',
    'Forbidden',
    'BadRequest',
    'NotFound',
    'AniListServerError',
)

class HTTPException(Exception):
    def __init__(self, status: int, data: Union[str, Dict[str, Any]]) -> None:
        self.status = status
        errors: List[Dict[str, Any]] = []

        if isinstance(data, dict):
            error: Dict[str, Any] = data['errors'][0]
            message: str = error['message']

            if message == 'validation':
                validation: Dict[str, Any] = error['validation']

                self.message: str = list(validation.values())[0][0]
                errors = list(validation.values())
            else:
                self.message: str = error['message']

        else:
            self.message = data
        
        self.errors = errors
        super().__init__(f'({self.status}): {self.message}')

class BadRequest(HTTPException):
    pass

class Unauthorized(HTTPException):
    pass

class Forbidden(HTTPException):
    pass

class NotFound(HTTPException):
    pass

class AniListServerError(HTTPException):
    pass

ERROR_MAPPING: Dict[int, Type[HTTPException]] = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    500: AniListServerError
}