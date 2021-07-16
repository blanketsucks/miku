from typing import Dict, TypeVar, Callable, Optional
from operator import attrgetter

T = TypeVar('T')

class Data(list[T]):
    """
    A subclass of `list` implementing 2 helper methods.
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
            async with miku.AnilistClient() as client:
                anime = await client.fetch_anime('Bakemonogatari')
                character = anime.characters.find(lambda character: character.name.full == 'Episode')
                print(character)
            ```
        """
        for data in self:
            if check(data):
                return data

    def get(self, **attrs: Dict):
        """
        This function returns the first element meeting the one of the attributes passed in.\n
        To nest attributes (e.g `x.y`) pass it in like `x_y`.

        This can be used as an alternative to [Data.find](./data.md#miku.utils.Data.find)

        Args:
            **attrs: The attributes to search with.

        Example:
            ```py
            async with miku.AnilistClient() as client:
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