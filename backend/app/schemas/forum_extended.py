from typing import Optional
from pydantic import BaseModel


class ForumQuestionCreate(BaseModel):
    title: str
    category: str
    detail: str


class ForumQuestionUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    detail: Optional[str] = None


class ForumQuestionResponse(BaseModel):
    id: int
    title: str
    category: str
    author: str
    time: str
    replies: int
    votes: int
    detail: str
    created_at: Optional[str] = None


class ForumReplyCreate(BaseModel):
    content: str


class ForumReplyResponse(BaseModel):
    id: int
    question_id: int
    author: str
    time: str
    content: str
    created_at: Optional[str] = None


class ForumLikeCreate(BaseModel):
    question_id: int


class ForumLikeResponse(BaseModel):
    id: int
    question_id: int
    user_id: int
    created_at: Optional[str] = None


class ForumQuestionList(BaseModel):
    id: int
    title: str
    category: str
    author: str
    time: str
    replies: int
    votes: int
    detail: str
    created_at: Optional[str] = None
    replies_count: int
    likes_count: int
