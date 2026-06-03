"""Gebelik Asistanı sohbet şemaları."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class ChatMessageCreate(BaseModel):
    from_: Literal["baby", "me"] = Field(alias="from")
    text: str = Field(min_length=1)
    session_id: int

    model_config = {"populate_by_name": True}


class ChatMessageUpdate(BaseModel):
    text: str = Field(min_length=1)


class AssistantMessageRequest(BaseModel):
    text: str = Field(min_length=1)
