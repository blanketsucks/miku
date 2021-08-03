import datetime
from typing import List

from .utils import Data
from .user import User
from .media import _get_media

class ThreadCategory:
    def __init__(self, payload) -> None:
        self.name: str = payload['name']
        self.id: int = payload['id']

    def __repr__(self):
        return f'<ThreadCategory id={self.id} name={self.name!r}>'

class ThreadComment:
    def __init__(self, payload, session) -> None:
        self._payload = payload
        self._session = session

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
    def thread(self) -> 'Thread':
        return Thread(self._payload['thread'], self._session)

    @property
    def user(self) -> User:
        return User(self._payload['user'], self._session)

    @property
    def likes(self) -> Data[User]:
        return Data([User(like, self._session) for like in self._payload['likes']])
    
    @property
    def children(self) -> Data['ThreadComment']:
        return Data([ThreadComment(child, self._session) for child in self._payload['children']])

class Thread:
    def __init__(self, data, session) -> None:
        self._payload = data
        self._session = session

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
        return f'<Thread id={self.id} reply_count={self.reply_count} view_count={self.view_count} like_count={self.like_count}>'

    def __eq__(self, other):
        return self.id == other.id

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
    def media_categories(self):
        return [_get_media(c)(c, self._session) for c in self._payload['categories']]
    
    @property
    def owner(self) -> User:
        return User(self._payload['user'], self._session)

    @property
    def reply_user(self) -> User:
        return User(self._payload['replyUser'], self._session)

    @property
    def likes(self) -> Data[User]:
        return Data([User(like, self._session) for like in self._payload['likes']])
    
    async def fetch_comments(self):
        data = await self._session.get_thread_comments(self.id)
        comments = Data([ThreadComment(comment, self._session) for comment in data['data']['ThreadComment']])
        return comments

    def to_dict(self):
        return self._payload.copy()