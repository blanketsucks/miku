from __future__ import annotations
from typing import (
    Any,
    Dict, 
    Generator, 
    Generic, 
    List, 
    Optional, 
    TYPE_CHECKING, 
    Type, 
    TypeVar, 
)

if TYPE_CHECKING:
    from .http import HTTPHandler

T = TypeVar('T')

__all__ = (
    'Page',
    'Paginator'
)


class Page(Generic[T]):
    def __init__(
        self,
        type: str, 
        payload: Dict[str, Any], 
        model: Type[T], 
        http: HTTPHandler,
    ) -> None:
        self.payload = payload['Page'][type]
        self.info = payload['Page']['pageInfo']
        self.current_item = 0
        self.http = http
        self.model = model

    def __repr__(self):
        return '<Page number={0.number} entries={0.entries}>'.format(self)

    def __getitem__(self, idx: int) -> T:
        return self.model(self.payload[idx], self.http)

    def __iter__(self):
        return self

    def __next__(self) -> T:
        data = self.next()
        if not data:
            raise StopIteration

        return data

    @property
    def entries(self) -> int:
        return len(self.payload)

    @property
    def number(self) -> int:
        return self.info['currentPage']

    def next(self) -> Optional[T]:
        try:
            data = self.payload[self.current_item]
        except IndexError:
            return None

        self.current_item += 1
        return self.model(data, self.http)

    def current(self) -> T:
        data = self.payload[self.current_item]
        return self.model(data, self.http)

    def previous(self) -> T:
        if not self.current_item:
            index = 0
        else:
            index = self.current_item - 1

        data = self.payload[index]
        return self.model(data, self.http)

class Paginator(Generic[T]):
    def __init__(self, http: HTTPHandler, type: str, query: str, vars: Dict[str, Any], model: Type[T]) -> None:
        self.http = http
        self.query = query
        self.type = type
        self.vars = vars
        self.model = model
        self.has_next_page = True
        self.current_page = 0
        self.next_page = 1
        self.pages: Dict[int, Page[T]] = {}

    def get_page(self, page: int) -> Optional[Page[T]]:
        return self.pages.get(page)

    async def fetch_page(self, page: int) -> Optional[Page[T]]:
        vars = self.vars.copy()
        vars['page'] = page

        data = await self.http.request(self.query, variables=vars)
        if not data:
            return None

        return Page(self.type, data, self.model, self.http)

    async def next(self) -> Optional[Page[T]]:
        if not self.has_next_page:
            return None

        self.vars['page'] = self.next_page

        data = await self.http.request(self.query, variables=self.vars)
        if not data:
            return None

        page = data['Page']['pageInfo']

        self.has_next_page = page['hasNextPage']
        self.next_page = page['currentPage'] + 1
        self.current_page = page['currentPage']

        page = Page(self.type, data, self.model, self.http)
        self.pages[self.current_page] = page

        return page

    async def current(self) -> Optional[Page[T]]:
        data = await self.http.request(self.query, variables=self.vars)
        if not data:
            return None

        return Page(self.type, data, self.model, self.http)

    async def previous(self) -> Optional[Page[T]]:
        vars = self.vars.copy()
        page = self.current_page - 1

        if self.current_page == 0:
            page = 0

        vars['page'] = page
        data = await self.http.request(self.query, variables=self.vars)
        if not data:
            return None

        return Page(self.type, data, self.model, self.http)

    async def collect(self) -> List[T]:
        return [obj async for page in self for obj in page]

    def __await__(self) -> Generator[Any, None, List[T]]:
        return self.collect().__await__()

    def __aiter__(self):
        return self

    async def __anext__(self) -> Page[T]:
        data = await self.next()
        if not data:
            raise StopAsyncIteration

        return data