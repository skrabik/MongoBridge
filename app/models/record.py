from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class RecordCreate(BaseModel):
    payload: Dict[str, Any] = Field(default_factory=dict)


class RecordUpdate(BaseModel):
    payload: Optional[Dict[str, Any]] = None


class RecordPayloadAdd(BaseModel):
    payload: Dict[str, Any]


class RecordOut(BaseModel):
    id: str
    payload: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


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
