from typing import Any, AsyncIterator, Coroutine, Dict, Iterable, TypeVar, Callable, Optional, List, Union
from operator import attrgetter
import asyncio

T = TypeVar('T')

async def maybe_coroutine(f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    ret = f(*args, **kwargs)
    if asyncio.iscoroutine(ret):
        return await ret

    return ret

class Data(list[T]):
    """
    A subclass of `list` implementing 3 helper methods.
    """
    def find(self, check: Callable[[T], bool]) -> Optional[T]:
        """
        This function returns the first element meeting the `check` condition.

        Args:
            check: A callable which takes in a single parameter and returns a `bool.`

        Returns:
            The element found or None if nothing met the check.

        Example:
            ```py
            async with miku.AsyncAnilistClient() as client:
                anime = await client.fetch_anime('Bakemonogatari')
                character = anime.characters.find(lambda character: character.name.full == 'Episode')
                print(character)
            ```
        """
        for data in self:
            if check(data):
                return data

    async def filter(self, check: Callable[[T], Union[Coroutine[Any, Any, bool], bool]]) -> AsyncIterator[T]:
        """
        This function yields all elements meeting the `check` condition.

        Args:
            check: A callable (can be a coroutine function) which takes in a single parameter and returns a `bool.`

        Example:
            ```py
            async with miku.AsyncAnilistClient() as client:
                medias = await client.media('5-toubun no hanayome')
                async for media in medias.filter(lambda media: media.format == miku.MediaFormat.TV):
                    print(media)
            ```
        """
        for element in self:
            if await maybe_coroutine(check, element):
                yield element

    def get(self, **attrs: Dict):
        """
        This function returns the first element meeting the one of the attributes passed in.\n
        To nest attributes (e.g `x.y`) pass it in like `x_y`.

        This can be used as an alternative to [Data.find](./data.md#miku.utils.Data.find)

        Args:
            **attrs: The attributes to search with.

        Example:
            ```py
            async with miku.AsyncAnilistClient() as client:
                anime = await client.fetch_anime('Bakemonogatari')
                character = anime.characters.get(name_full='Episode')
                print(character)
            ```
        """
        converted = [(attrgetter(attr.replace('_', '.')), value) for attr, value in attrs.items()]

        for obj in self:
            if any(check(obj) == value for check, value in converted):
                return obj
             
        return None

def remove_docstring(f):
    f.__doc__ = ''
    return f

async def map(func: Callable[[T], Coroutine[Any, Any, Any]], iterable: Iterable[T]) -> AsyncIterator:
    for iterable in iterable:
        yield await func(iterable)