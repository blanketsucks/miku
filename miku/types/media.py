from __future__ import annotations

from typing import List, Optional, TypedDict, TYPE_CHECKING

from .image import Image

if TYPE_CHECKING:
    from .nodes import CharacterNodes

__all__ = (
    'MediaTrend',
    'MediaTitle',
    'MediaTrailer',
    'MediaTag',
    'MediaAiringSchedule',
    'MediaStreamingEpisode',
    'MediaRank',
    'Media',
)

class MediaTrend(TypedDict):
    mediaId: int
    date: int
    trending: int
    averageScore: int
    popularity: int
    inProgress: int
    releasing: bool
    episode: int

class MediaTitle(TypedDict):
    romaji: str
    english: Optional[str]
    native: str

class MediaTrailer(TypedDict):
    id: str
    site: str
    thumbnail: str

class MediaTag(TypedDict):
    id: int
    name: str
    category: str
    description: str
    rank: int
    isGeneralSpoiler: bool
    isMediaSpoiler: bool
    isAdult: bool
    userId: int

class MediaAiringSchedule(TypedDict):
    id: int
    episode: int
    mediaId: int
    airingAt: int
    timeUntilAiring: int

class MediaStreamingEpisode(TypedDict):
    title: str
    thumbnail: str
    url: str
    site: str

class MediaRank(TypedDict):
    rank: int
    id: int
    year: int
    allTime: bool
    context: str
    type: str
    format: str
    season: str

class Media(TypedDict):
    id: int
    idMal: int
    siteUrl: str
    averageScore: int
    meanScore: int
    isLicensed: bool
    genres: List[str]
    trending: int
    isAdult: bool
    synonyms: List[str]
    description: str
    hashtag: str
    popularity: int
    favourites: int
    type: str
    format: str
    season: str
    status: str
    source: str
    duration: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    episodes: Optional[int]
    updatedAt: int
    title: MediaTitle
    tags: List[MediaTag]
    trailer: Optional[MediaTrailer]
    nextAiringEpisode: Optional[MediaAiringSchedule]
    streamingEpisodes: Optional[List[MediaStreamingEpisode]]
    rankings: List[MediaRank]
    bannerImage: str
    coverImage: Image
    characters: CharacterNodes