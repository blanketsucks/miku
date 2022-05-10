from __future__ import annotations

from typing import (
    TYPE_CHECKING, 
    Any,
    Callable, 
    Coroutine, 
    Generic,
    Iterator, 
    List, 
    Optional, 
    TypeVar, 
    Type, 
    overload, 
    Union
)
import asyncio

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    P = ParamSpec('P')

__all__ = (
    'IDComparable',
    'CachedSlotProperty',
    'cached_slot_property',
    'maybe_coroutine',
    'find',
)

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)

Coro = Coroutine[Any, Any, T]
MaybeAwaitable = Union[T, Coroutine[Any, Any, T]]

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

async def maybe_coroutine(func: Callable[P, MaybeAwaitable[T]], *args: P.args, **kwargs: P.kwargs) -> T:
    ret = func(*args, **kwargs)
    if asyncio.iscoroutine(ret):
        return await ret

    return ret # type: ignore
    
def find(iterable: Iterator[T], predicate: Callable[[T], bool]) -> List[T]:
    return [item for item in iterable if predicate(item)]

