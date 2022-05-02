from typing import Optional, TypedDict

__all__ = 'Image',

class Image(TypedDict):
    large: Optional[str]
    medium: Optional[str]