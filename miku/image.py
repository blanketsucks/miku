from typing import Union, Dict
from aiohttp import ClientSession

class Image:
    def __init__(self, session: ClientSession, payload: Union[Dict[str, str], str]) -> None:
        self._session = session 
    
        if isinstance(payload, str):
            self.large = payload
            self.medium = None
        else:
            self.large = payload.get("large")
            self.medium = payload.get("medium")

    async def read(self, large: bool = True, medium: bool = False) -> bytes:
        """
        Reads the image.

        Args:
            large: Whether to read `large` image.
            medium: Whether to read `medium` image.

        Returns:
            image's bytes.
        """
        if large and medium:
            raise ValueError("Cannot set both large and medium to True")

        if not large and not medium:
            raise ValueError("Cannot set both large and medium to False")

        if large:
            url = self.large

        if medium:
            url = self.medium

        async with self._session.get(url) as response:
            data = await response.read()
            return data

    async def save(self, fp: str, *, large: bool = True, medium: bool = False) -> int:
        """
        Saves the image.

        Args:
            fp: a string with file name and extension.
            large: Whether to save `large` image.
            medium: Whether to save `medium` image.

        Returns:
            Number of bytes written.
        """
        data = await self.read(large=large, medium=medium)

        with open(fp, "wb") as file:
            return file.write(data)
