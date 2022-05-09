from __future__ import annotations

from typing import Any, Dict, Optional, TypedDict, List, TYPE_CHECKING

from .image import Image

if TYPE_CHECKING:
    from .media import MediaTag, Media
    from .staff import Staff
    from .studio import Studio
    from .nodes import CharacterNodes, AnimeNodes, MangaNodes, StaffNodes, StudioNodes

__all__ = (
    'MediaList',
    'MediaListGroup',
    'UserNotificationOption',
    'ListActivityOption',
    'UserOptions',
    'MediaListTypeOptions',
    'MediaListOptions',
    'UserStatistics',
    'UserStatisticsType',
    'UserFavourites',
    'User',
)

class MediaList(TypedDict):
    id: int
    userId: int
    mediaId: int
    status: str
    score: int
    progress: int
    progressVolumes: int
    repeat: int
    priority: int
    private: bool
    notes: str
    hiddenFromStatusLists: bool
    customLists: Any
    advancedScores: Any
    updatedAt: int
    createdAt: int
    media: Media

class MediaListGroup(TypedDict):
    name: str
    isCustomList: bool
    isSplitCompletedList: bool
    status: str
    entries: List[MediaList]

class UserNotificationOption(TypedDict):
    enabled: bool
    type: str

class ListActivityOption(TypedDict):
    disabled: bool
    type: str

class UserOptions(TypedDict):
    titleLanguage: str
    displayAdultContent: bool
    airingNotifications: bool
    profileColor: str
    notificationOptions: List[UserNotificationOption]
    timezone: str
    activityMergeTime: int
    staffNameLanguage: str
    restrictMessagesToFollowing: bool

class MediaListTypeOptions(TypedDict):
    sectionOrder: List[str]
    splitCompletedSectionByFormat: bool
    customLists: List[str]
    advancedScoring: List[str]
    advancedScoringEnabled: bool

class MediaListOptions(TypedDict):
    scoreFormat: str
    rowOrder: str
    animeList: MediaListTypeOptions
    mangaList: MediaListTypeOptions

class _UserStatistic(TypedDict):
    count: Optional[int]
    meanScore: Optional[float]
    minutesWatched: Optional[int]
    chaptersRead: Optional[int]
    mediaIds: List[int]

class UserFormatStatistic(_UserStatistic):
    format: str

class UserStatusStatistic(_UserStatistic):
    status: str

class UserScoreStatistic(_UserStatistic):
    score: int

class UserLengthStatistic(_UserStatistic):
    length: str

class UserReleaseYearStatistic(_UserStatistic):
    releaseYear: int

class UserStartYearStatistic(_UserStatistic):
    startYear: int

class UserGenreStatistic(_UserStatistic):
    genre: str

class UserTagStatistic(_UserStatistic):
    tag: MediaTag

class UserCountryStatistic(_UserStatistic):
    country: str

class UserVoiceActorStatistic(_UserStatistic):
    voiceActor: Staff
    characterIds: List[int]

class UserStaffStatistic(_UserStatistic):
    staff: Staff

class UserStudioStatistic(_UserStatistic):
    studio: Studio

class UserStatistics(TypedDict):
    count: Optional[int]
    meanScore: Optional[float]
    standardDeviation: Optional[float]
    minutesWatched: Optional[int]
    episodesWatched: Optional[int]
    chaptersRead: Optional[int]
    volumesRead: Optional[int]
    formats: List[UserFormatStatistic]
    statuses: List[UserStatusStatistic]
    scores: List[UserScoreStatistic]
    lengths: List[UserLengthStatistic]
    releaseYears: List[UserReleaseYearStatistic]
    startYears: List[UserStartYearStatistic]
    genres: List[UserGenreStatistic]
    tags: List[UserTagStatistic]
    countries: List[UserCountryStatistic]
    voiceActors: List[UserVoiceActorStatistic]
    staff: List[UserStaffStatistic]
    studios: List[UserStudioStatistic]

class UserStatisticsType(TypedDict):
    anime: UserStatistics
    manga: UserStatistics

class UserFavourites(TypedDict):
    anime: AnimeNodes
    manga: MangaNodes
    characters: CharacterNodes
    staff: StaffNodes
    studios: StudioNodes

class User(TypedDict):
    id: int
    name: str
    about: str
    siteUrl: str
    options: UserOptions
    bannerImage: str
    avatar: Image
    bans: List[Dict[str, Any]]
    mediaListOptions: MediaListOptions
    statistics: UserStatisticsType
    favourites: UserFavourites
    unreadNotificationCount: int
    donatorTier: int
    donatorBadge: str
    moderatorRoles: Optional[List[str]]