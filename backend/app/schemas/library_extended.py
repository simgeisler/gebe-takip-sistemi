from typing import Optional
from pydantic import BaseModel


class LibraryArticleCreate(BaseModel):
    title: str
    category: str
    description: str
    read_minutes: int
    body: str
    image_url: Optional[str] = None


class LibraryArticleUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    read_minutes: Optional[int] = None
    body: Optional[str] = None
    image_url: Optional[str] = None


class LibraryArticleResponse(BaseModel):
    id: int
    title: str
    category: str
    description: Optional[str] = None
    read_minutes: int
    body: Optional[str] = None
    image_url: Optional[str] = None
    created_at: Optional[str] = None
    likes_count: int = 0
    liked_by_me: bool = False


class LibraryArticleList(BaseModel):
    id: int
    title: str
    category: str
    description: Optional[str] = None
    read_minutes: int
    image_url: Optional[str] = None
    created_at: Optional[str] = None
    likes_count: int


class LibraryLikeCreate(BaseModel):
    article_id: int


class LibraryLikeResponse(BaseModel):
    id: int
    article_id: int
    user_id: int
    created_at: str
