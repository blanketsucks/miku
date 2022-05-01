from typing import Any, Dict, List
import datetime

__all__ = (
    'SiteTrend',
    'SiteStatistics'
)

class SiteTrend:
    __slots__ = ('_payload', 'count', 'change')

    def __init__(self, payload: Dict[str, Any]) -> None:
        self._payload = payload

        self.count: int = payload['count']
        self.change: int = payload['change']
    
    @property
    def date(self) -> datetime.datetime:
        """
        The day the data was recorded

        Returns:
            A `datetime.datetime` object.
        """
        return datetime.datetime.utcfromtimestamp(self._payload['date'])
    
    def __repr__(self) -> str:
        return '<SiteTrend count={0.count} change={0.change}>'.format(self)

class SiteStatistics:
    __slots__ = ('_payload',)

    def __init__(self, payload: Dict[str, Any]) -> None:
        self._payload = payload

    @property
    def users(self) -> List[SiteTrend]:
        """
        User statistics.

        Returns:
            A list of [SiteTrend](./site-statistics.md)s.
        """
        users = self._payload['users']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def anime(self) -> List[SiteTrend]:
        """
        Anime statistics.

        Returns:
            A list of [SiteTrend](./site-statistics.md)s.
        """
        users = self._payload['anime']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def manga(self) -> List[SiteTrend]:
        """
        Manga statistics.

        Returns:
            A list of [SiteTrend](./site-statistics.md)s.
        """
        users = self._payload['manga']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def characters(self) -> List[SiteTrend]:
        """
        Character statistics.

        Returns:
            A list of [SiteTrend](./site-statistics.md)s.
        """
        users = self._payload['characters']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def studios(self) -> List[SiteTrend]:
        """
        Studio statistics.

        Returns:
            A list of [SiteTrend](./site-statistics.md)s.
        """
        users = self._payload['studios']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def staff(self) -> List[SiteTrend]:
        """
        Staff statistics.

        Returns:
            A list of [SiteTrend](./site-statistics.md)s.
        """
        users = self._payload['staff']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def reviews(self) -> List[SiteTrend]:
        """
        Review statistics.

        Returns:
            A list of [SiteTrend](./site-statistics.md)s.
        """
        users = self._payload['reviews']['nodes']
        return [SiteTrend(user) for user in users]
    
