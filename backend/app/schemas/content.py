from pydantic import BaseModel, Field


class LibraryArticleCreate(BaseModel):
    """Library.tsx kartı + detay: cat, title, desc, time (read_minutes), body."""

    cat: str = Field(min_length=1)
    title: str = Field(min_length=1)
    desc: str = Field(min_length=1)
    body: str = ""
    read_minutes: int = Field(default=5, ge=1)


class LibraryArticleUpdate(BaseModel):
    cat: str | None = None
    title: str | None = None
    desc: str | None = None
    body: str | None = None
    read_minutes: int | None = Field(default=None, ge=1)
