from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AuditLogBase(BaseModel):
    entity_type: str
    entity_id: str
    user_id: int | None
    action: str
    previous_state: dict[str, Any] | None
    new_state: dict[str, Any] | None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogResponse(AuditLogBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
