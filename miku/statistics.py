from typing import List
import datetime

from . import types

__all__ = (
    'SiteTrend',
    'SiteStatistics'
)

class SiteTrend:
    __slots__ = ('_payload', 'count', 'change')

    def __init__(self, payload: types.SiteTrend) -> None:
        self._payload = payload

        self.count: int = payload['count']
        self.change: int = payload['change']
    
    @property
    def date(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._payload['date'])
    
    def __repr__(self) -> str:
        return '<SiteTrend count={0.count} change={0.change}>'.format(self)

class SiteStatistics:
    __slots__ = ('_payload',)

    def __init__(self, payload: types.SiteStatistics) -> None:
        self._payload = payload

    @property
    def users(self) -> List[SiteTrend]:
        users = self._payload['users']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def anime(self) -> List[SiteTrend]:
        users = self._payload['anime']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def manga(self) -> List[SiteTrend]:
        users = self._payload['manga']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def characters(self) -> List[SiteTrend]:
        users = self._payload['characters']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def studios(self) -> List[SiteTrend]:
        users = self._payload['studios']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def staff(self) -> List[SiteTrend]:
        users = self._payload['staff']['nodes']
        return [SiteTrend(user) for user in users]

    @property
    def reviews(self) -> List[SiteTrend]:
        users = self._payload['reviews']['nodes']
        return [SiteTrend(user) for user in users]

