from pydantic import BaseModel, ConfigDict, Field

from src.models.user import UserRole


class UserBase(BaseModel):
    ad_soyad: str = Field(min_length=3, max_length=150)
    email: str = Field(min_length=5, max_length=255)
    rol: UserRole = UserRole.MEMBER


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
