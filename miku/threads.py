from __future__ import annotations

from typing import Dict, List, Any, TYPE_CHECKING
import datetime

from .user import User
from .media import Media
from .utils import IDComparable, cached_slot_property
from . import types

if TYPE_CHECKING:
    from .http import HTTPHandler

__all__ = (
    'ThreadCategory',
    'ThreadComment',
    'Thread'
)

class ThreadCategory(IDComparable):
    __slots__ = ('name', 'id')

    def __init__(self, payload: types.ThreadCategory) -> None:
        self.name: str = payload['name']
        self.id: int = payload['id']

    def __repr__(self):
        return f'<ThreadCategory id={self.id} name={self.name!r}>'

class ThreadComment(IDComparable):
    __slots__ = (
        '_payload',
        '_http',
        '_cs_children',
        'id',
        'user_id',
        'thread_id',
        'comment',
        'like_count',
        'is_liked',
        'url'
    )

    def __init__(self, payload: types.ThreadComment, http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.id: int = payload['id']
        self.user_id: int = payload['userId']
        self.thread_id: int = payload['threadId']
        self.comment: str = payload['comment']
        self.like_count: int = payload['likeCount']
        self.is_liked: bool = payload['isLiked']
        self.url: str = payload['siteUrl']

    def __repr__(self) -> str:
        return f'<ThreadComment id={self.id} user_id={self.user_id} thread_id={self.thread_id}>'

    @property
    def created_at(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._payload['createdAt'])

    @property
    def updated_at(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._payload['updatedAt'])

    @property
    def thread(self) -> Thread:
        return Thread(self._payload['thread'], self._http)

    @property
    def user(self) -> User:
        return User(self._payload['user'], self._http)

    @property
    def likes(self) -> List[User]:
        return [User(like, self._http) for like in self._payload['likes']]
    
    @cached_slot_property('_cs_children')
    def children(self) -> List[ThreadComment]:
        return [ThreadComment(child, self._http) for child in self._payload['childComments']]

class Thread(IDComparable):
    __slots__ = (
        '_payload',
        '_http',
        '_cs_likes',
        '_cs_media_categories',
        'id',
        'url',
        'title',
        'body',
        'user_id',
        'reply_user_id',
        'reply_comment_id',
        'reply_count',
        'view_count',
        'is_locked',
        'is_sticky',
        'is_subscribed',
        'is_liked',
        'like_count'
    )

    def __init__(self, payload: types.Thread, http: HTTPHandler) -> None:
        self._payload = payload
        self._http = http

        self.id: int = self._payload['id']
        self.url: str = self._payload['siteUrl']
        self.title: str = self._payload['title']
        self.body: str = self._payload['body']
        self.user_id: int = self._payload['userId']
        self.reply_user_id: int = self._payload['replyUserId']
        self.reply_comment_id: int = self._payload['replyCommentId']
        self.reply_count: int = self._payload['replyCount']
        self.view_count: int = self._payload['viewCount']
        self.is_locked: bool = self._payload['isLocked']
        self.is_sticky: bool = self._payload['isSticky']
        self.is_subscribed: bool = self._payload['isSubscribed']
        self.is_liked: bool = self._payload['isLiked']
        self.like_count: int = self._payload['likeCount']

    def __repr__(self) -> str:
        return f'<Thread id={self.id} is_locked={self.is_locked}>'

    @property
    def replied_at(self):
        return datetime.datetime.utcfromtimestamp(self._payload['repliedAt'])

    @property
    def created_at(self):
        return datetime.datetime.utcfromtimestamp(self._payload['createdAt'])

    @property
    def updated_at(self):
        return datetime.datetime.utcfromtimestamp(self._payload['updatedAt'])

    @property
    def categories(self) -> List[ThreadCategory]:
        return [ThreadCategory(c) for c in self._payload['categories']]

    @property
    def owner(self) -> User:
        return User(self._payload['user'], self._http)

    @property
    def reply_user(self) -> User:
        return User(self._payload['replyUser'], self._http)

    @cached_slot_property('_cs_likes')
    def likes(self) -> List[User]:
        return [User(like, self._http) for like in self._payload['likes']]

    @cached_slot_property('_cs_media_categories')
    def media_categories(self) -> List[Media]:
        return [Media(c, self._http) for c in self._payload['mediaCategories']]
    
    async def fetch_comments(self) -> List[ThreadComment]:
        data = await self._http.get_thread_comments(self.id)
        return [ThreadComment(comment, self._http) for comment in data]
