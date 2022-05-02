from __future__ import annotations

from typing import TypedDict, List

from .media import Media
from .user import User

__all__ = (
    'ThreadCategory',
    'ThreadComment',
    'Thread'
)

class ThreadCategory(TypedDict):
    id: int
    name: str

class ThreadComment(TypedDict):
    id: int
    userId: int
    threadId: int
    comment: str
    likeCount: int
    isLiked: bool
    siteUrl: str
    createdAt: int
    updatedAt: int
    childComments: List[ThreadComment]
    likes: List[User]
    user: User
    thread: Thread

class Thread(TypedDict):
    id: int
    siteUrl: str
    title: str
    body: str
    userId: int
    replyUserId: int
    replyCommentId: int
    replyCount: int
    viewCount: int
    likeCount: int
    isLocked: bool
    isSticky: bool
    isSubscribed: bool
    isLiked: bool
    createdAt: int
    updatedAt: int
    repliedAt: int
    categories: List[ThreadCategory]
    mediaCategories: List[Media]
    likes: List[User]
    replyUser: User
    user: User