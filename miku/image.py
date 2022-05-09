from __future__ import annotations

from typing import Any
from aiohttp import ClientSession

from . import types

__all__ = (
    'Image',
)

class Image:
    __slots__ = ('_session', 'large', 'medium')

    def __init__(self, session: ClientSession, payload: types.Image) -> None:
        self._session = session 
    
        self.large = payload['large']
        self.medium = payload.get('medium')

    @classmethod
    def from_url(cls, session: ClientSession, url: str) -> Image:
        payload: Any = {'large': url, 'medium': None}
        return cls(session, payload)
        
    async def read(self, large: bool = True, medium: bool = False) -> bytes:
        if large and medium:
            raise ValueError('Cannot set both large and medium to True')

        if not large and not medium:
            raise ValueError('Cannot set both large and medium to False')

        if medium:
            assert self.medium, 'No medium image available'
            url = self.medium
        else:
            url = self.large
        
        async with self._session.get(url) as response:
            data = await response.read()
            return data

    async def save(self, fp: str, *, large: bool = True, medium: bool = False) -> int:
        data = await self.read(large=large, medium=medium)

        with open(fp, 'wb') as file:
            return file.write(data)
