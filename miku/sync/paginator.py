from __future__ import annotations

from typing import (
    Any,
    Dict, 
    Generic, 
    List, 
    Optional, 
    TYPE_CHECKING, 
    Type, 
    TypeVar, 
)
import aiohttp

from .utils import Data

if TYPE_CHECKING:
    from .http import SyncHTTPHandler

T = TypeVar('T')

__all__ = (
    'Page',
    'Paginator'
)


class Page(Data[T]):
    """
    A subclass of [Data](./data.md) that represents a page of data returned by a [Paginator](./paginator.md).
    """
    def __init__(self,
                type: str, 
                payload: Dict[str, Any], 
                model: Type, 
                session: aiohttp.ClientSession,
                cls: Type) -> None:
        self.cls = cls
        self.payload = payload['data']['Page'][type]
        self.info = payload['data']['Page']['pageInfo']
        self.current_item = 0
        self.session = session
        self.model = model

        super().__init__(self.payload)

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
        return self.model(payload=data, session=self.session, cls=self.cls)

    def current(self) -> T:
        """
        Returns the current element on this page.

        Returns:
            The current element on this page.
        """
        data = self.payload[self.current_item]
        return self.model(payload=data, session=self.session)

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
        return self.model(payload=data, session=self.session)

class Paginator(Generic[T]):
    def __init__(self, http: SyncHTTPHandler, type: str, query: str, vars: Dict[str, Any], model: Type, image_cls) -> None:
        self.http = http
        self.cls = image_cls
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

    def fetch_page(self, page: int) -> Optional[Page[T]]:
        vars = self.vars.copy()
        vars['page'] = page

        json = self.http.request(self.query, vars)
        data = json['data']

        if not data:
            return None

        return Page(self.type, json, self.model, self.http.session, self.cls)

    def next(self) -> Optional[Page[T]]:
        """
        Fetches the next page.

        Returns:
            a [Page](./page.md) object or None.
        """

        if not self.has_next_page:
            return None

        self.vars['page'] = self.next_page

        json = self.http.request(self.query, self.vars)
        data = json['data']
        if not data:
            return None

        page = data['Page']['pageInfo']

        self.has_next_page = page['hasNextPage']
        self.next_page = page['currentPage'] + 1
        self.current_page = page['currentPage']

        page = Page(self.type, json, self.model, self.http.session, self.cls)
        self.pages[self.current_page] = page

        return page

    def current(self) -> Optional[Page[T]]:
        """
        Fetches the current page.

        Returns:
            a [Page](./page.md) object or None.
        """
        json = self.http.request(self.query, self.vars)
        data = json['data']

        if not data:
            return None

        return Page(self.type, json, self.model, self.http.session, self.cls)

    def previous(self) -> Optional[Page[T]]:
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
        json = self.http.request(self.query, vars)
        data = json['data']
        
        if not data:
            return None

        return Page(self.type, json, self.model, self.http.session, self.cls)

    def collect(self) -> List[Page[T]]:
        """
        Collects all the fetchable pages and returns them as a list

        Args:
            get_page_data: A bool indiacting whether to get the data from the fetched page or not.

        Returns:
            A list containing [Page](./page.md) objects.   
        """

        pages = []

        while True:
            page = self.next()
            if not page:
                break

            pages.append(page)

        return pages

    def __iter__(self) -> Paginator[T]:
        """
        Returns:
            This same [Paginator](./paginator.md) object.
        """
        return self

    def __next__(self) -> Page[T]:
        """
        Returns:
            The next [Page](./page.md).
        """
        data = self.next()
        if not data:
            raise StopIteration

        return data