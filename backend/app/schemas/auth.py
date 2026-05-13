from datetime import date
from typing import Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    """Kayıt: frontend `sat`/`kilo` gönderir; eski istemciler `last_menstrual_period`/`starting_weight` kullanabilir."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=8)
    sat: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("sat", "last_menstrual_period"),
    )
    expected_due_date: Optional[str] = None
    kilo: float = Field(
        ...,
        gt=0,
        validation_alias=AliasChoices("kilo", "starting_weight"),
    )


class LoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    password: str


class UserProfileUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(default=None, min_length=2)
    sat: Optional[date] = Field(None, alias="last_menstrual_period")
    kilo: Optional[float] = Field(default=None, gt=0, alias="starting_weight")
