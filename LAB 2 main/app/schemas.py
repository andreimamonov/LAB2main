from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

# ----- Базовые схемы для Item -----
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    status: str = Field(default="active", pattern="^(active|inactive)$")

# Схема для создания (наследует ItemBase, все поля обязательны как в базовой)
class ItemCreate(ItemBase):
    pass

# Схема для обновления (все поля опциональны)
class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(active|inactive)$")

# Схема для ответа (содержит все поля, включая id и метки времени)
class ItemResponse(ItemBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # позволяет создавать схему из ORM-объекта (ранее orm_mode)

# ----- Схемы для пагинации -----
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)

class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int

class PaginatedResponse(BaseModel):
    data: list[ItemResponse]
    meta: PaginationMeta