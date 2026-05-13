"""BabyChat.tsx: from baby | me."""

from typing import Literal

from pydantic import BaseModel, Field


class ChatMessageCreate(BaseModel):
    from_: Literal["baby", "me"] = Field(alias="from")
    text: str = Field(min_length=1)

    model_config = {"populate_by_name": True}


class ChatMessageUpdate(BaseModel):
    text: str = Field(min_length=1)
