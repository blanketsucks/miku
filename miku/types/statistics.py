from typing import List, TypedDict

__all__ = (
    'SiteTrend',
    'SiteTrendNodes',
    'SiteStatistics'
)

class SiteTrend(TypedDict):
    count: int
    change: int
    date: int

class SiteTrendNodes(TypedDict):
    nodes: List[SiteTrend]

class SiteStatistics(TypedDict):
    users: SiteTrendNodes
    anime: SiteTrendNodes
    manga: SiteTrendNodes
    characters: SiteTrendNodes
    staff: SiteTrendNodes
    reviews: SiteTrendNodes
    studios: SiteTrendNodes
