from pydantic import BaseModel, Field


class ForumThreadCreate(BaseModel):
    """Forum.tsx — Yeni Başlık: cat + title + isteğe bağlı gövde."""

    cat: str = Field(min_length=1)
    title: str = Field(min_length=1)
    body: str = ""


class ForumThreadUpdate(BaseModel):
    cat: str | None = None
    title: str | None = None
    body: str | None = None
