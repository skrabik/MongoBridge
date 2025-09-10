from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field

class UserDataCreate(BaseModel):
    conversation_id: str
    data: Dict[str, Any] = Field(default_factory=dict)


class UserDataPatch(BaseModel):
    data: Dict[str, Any]


class UserDataOut(BaseModel):
    conversation_id: str
    data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
