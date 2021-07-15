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
    Union
)
import aiohttp

if TYPE_CHECKING:
    from .http import HTTPHandler

T = TypeVar('T')

__all__ = (
    'Page',
    'Paginator'
)

class Page(Generic[T]):
    def __init__(self,
                type: str, 
                payload: Dict[str, Any], 
                model: Type, 
                session: aiohttp.ClientSession) -> None:
        self.payload = payload['data']['Page'][type]
        self.info = payload['data']['Page']['pageInfo']
        self.current_item = 0
        self.session = session
        self.model = model

    def __repr__(self):
        return '<Page number={0.number} entries={0.entries}>'.format(self)

    def __iter__(self) -> Page[T]:
        """
        Returns:
            This same [Page](./page.md) object.
        """
        return self

    def __next__(self) -> T:
        """
        Returns:
            The next element on this page.
        """
        data = self.next()
        if not data:
            raise StopIteration

        return data

    @property
    def entries(self) -> int:
        """
        Returns the number of data entries are in this page.

        Returns:
            Number of entries.

        """
        return len(self.payload)

    @property
    def number(self) -> int:
        """
        Returns the current page number.

        Returns:
            Page number.
        
        """
        return self.info['currentPage']

    def next(self) -> Optional[T]:
        """
        Returns the next element on this page.

        Returns:
            The next element on this page.
        """

        try:
            data = self.payload[self.current_item]
        except IndexError:
            return None

        self.current_item += 1
        return self.model(data, session=self.session)

    def current(self) -> T:
        """
        Returns the current element on this page.

        Returns:
            The current element on this page.
        """
        data = self.payload[self.current_item]
        return self.model(data, session=self.session)

    def previous(self) -> T:
        """
        Returns the previous element on this page.

        Returns:
            The previous element on this page.
        """
        index = self.current_item -1

        if self.current_item == 0:
            index = 0

        data = self.payload[index]
        return self.model(data, session=self.session)

    def collect(self) -> List[T]:
        """
        Collects all the elements inside this page and returns them as a list

        Returns:
            A list containing all the elements of this page.   
        """

        data = []
        while True:
            ret = self.next()
            if not ret:
                break

            data.append(ret)

        return data

class Paginator(Generic[T]):
    def __init__(self, http: HTTPHandler, type: str, query: str, vars: Dict[str, Any], model: Type) -> None:
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
        """
        Returns the page with that number if available.

        Args:
            page: The number of the page.

        Returns:
            a [Page](./page.md) object or None.
        """

        return self.pages.get(page)

    async def next(self) -> Optional[Page[T]]:
        """
        Fetches the next page.

        Returns:
            a [Page](./page.md) object or None.
        """

        if not self.has_next_page:
            return None

        self.vars['page'] = self.next_page

        json = await self.http.request(self.query, self.vars)
        data = json['data']
        if not data:
            return None

        page = data['Page']['pageInfo']

        self.has_next_page = page['hasNextPage']
        self.next_page = page['currentPage'] + 1
        self.current_page = page['currentPage']

        page = Page(self.type, json, self.model, self.http.session)
        self.pages[self.current_page] = page

        return page

    async def current(self) -> Optional[Page[T]]:
        """
        Fetches the current page.

        Returns:
            a [Page](./page.md) object or None.
        """
        json = await self.http.request(self.query, self.vars)
        data = json['data']

        if not data:
            return None

        return Page(self.type, json, self.model, self.http.session)

    async def previous(self) -> Optional[Page[T]]:
        """
        Fetches the previous page.

        Returns:
            a [Page](./page.md) object or None.
        """
        vars = self.vars.copy()
        page = self.current_page - 1

        if self.current_page == 0:
            page = 0

        vars['page'] = page
        json = await self.http.request(self.query, vars)
        data = json['data']
        
        if not data:
            return None

        return Page(self.type, json, self.model, self.http.session)

    async def collect(self, get_page_data: bool=False) -> Union[List[Page[T], List[T]]]:
        """
        Collects all the fetchable pages and returns them as a list

        Args:
            get_page_data: A bool indiacting whether to get the data from the fetched page or not.

        Returns:
            A list containing [Page](./page.md) objects or [Page](./page.md) elements.   
        """

        def collect(pages, page):
            if get_page_data:
                return pages.extend(page.collect())

            pages.append(page)

        pages = []

        while True:
            page = await self.next()
            if not page:
                break

            collect(pages, page)

        return pages

    def __await__(self) -> Generator[Any, None, List[T]]:
        return self.collect(get_page_data=True).__await__()

    def __aiter__(self) -> Paginator[T]:
        """
        Returns:
            This same [Paginator](./paginator.md) object.
        """
        return self

    async def __anext__(self) -> Page[T]:
        """
        Returns:
            The next [Page](./page.md).
        """
        data = await self.next()
        if not data:
            raise StopAsyncIteration

        return data