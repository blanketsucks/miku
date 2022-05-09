from typing import Optional, TypedDict

__all__ = 'Image',

class Image(TypedDict):
    large: str
    medium: Optional[str]