from typing import List, Literal

from pydantic import BaseModel


NotificationType = Literal["comment", "like"]


class NotificationResponse(BaseModel):
    id: int
    type: NotificationType
    actor_name: str
    question_id: int
    question_title: str
    is_read: bool
    time_label: str
    created_at: str | None = None


class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    unread_count: int


class UnreadCountResponse(BaseModel):
    unread_count: int
