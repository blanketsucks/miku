from __future__ import annotations
from ctypes import Union

from typing import Any, Callable, Generic, Optional, TypeVar, Type, overload

__all__ = (
    'IDComparable',
    'CachedSlotProperty',
    'cached_slot_property',
)

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)

class IDComparable:
    id: Any

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

class CachedSlotProperty(Generic[T, T_co]):
    def __init__(self, name: str, func: Callable[[T], T_co]) -> None:
        self.name = name
        self.func = func
        self.__doc__ = getattr(func, '__doc__')

    @overload
    def __get__(self, instance: None, owner: Type[T]) -> CachedSlotProperty[T, T_co]:
        ...
    @overload
    def __get__(self, instance: T, owner: Type[T]) -> T_co:
        ...
    def __get__(self, instance: Optional[T], owner: Type[T]) -> Any:
        if instance is None:
            return self

        try:
            value = getattr(instance, self.name)
        except AttributeError:
            value = self.func(instance)
            setattr(instance, self.name, value)

        return value

def cached_slot_property(name: str) -> Callable[[Callable[[T], T_co]], CachedSlotProperty[T, T_co]]:
    def decorator(func: Callable[[T], T_co]) -> CachedSlotProperty[T, T_co]:
        return CachedSlotProperty(name, func)
    return decorator
    