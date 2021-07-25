from typing import Any, Dict, Type, Union

__all__ = (
    'HTTPException',
    'Forbidden',
    'BadRequest'
)

class HTTPException(Exception):
    status: int = None
    def __init__(self, data: Union[str, Dict[str, Any]]) -> None:
        if isinstance(data, dict):
            error: Dict[str, Any] = data['errors'][0]

            if not self.status:
                self.status: int = error['status']

            message: str = error['message']

            if message == 'validation':
                validation: Dict[str, Any] = error['validation']

                self.message: str = validation.values()[0][0]
                self.errors = list(validation.values())
            else:
                self.message: str = error['message']
                self.errors = []

        else:
            self.message = data
            self.errors = []
        
        if self.status:
            ret = f'{self.status}: {self.message}'
        else:
            ret = self.message

        super().__init__(ret)

class BadRequest(HTTPException):
    status = 400

class Forbidden(HTTPException):
    status = 403

class AniListServerError(HTTPException):
    pass

mapping: Dict[int, Type[HTTPException]] = {
    400: BadRequest,
    403: Forbidden,
    500: AniListServerError
}