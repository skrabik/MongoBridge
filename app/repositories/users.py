from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional, List

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument


def _serialize_user(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "conversation_id": doc.get("conversation_id"),
        "data": doc.get("data", {}),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }


async def upsertUserData(col: AsyncIOMotorCollection, conversation_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    res = await col.find_one_and_update(
        {"conversation_id": conversation_id},
        {
            "$setOnInsert": {"conversation_id": conversation_id, "created_at": now},
            "$set": {"data": data, "updated_at": now},
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return _serialize_user(res)


async def mergeUserData(col: AsyncIOMotorCollection, conversation_id: str, data_patch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    set_update: Dict[str, Any] = {f"data.{k}": v for k, v in data_patch.items()}
    set_update["updated_at"] = now
    res = await col.find_one_and_update(
        {"conversation_id": conversation_id},
        {"$set": set_update, "$setOnInsert": {"conversation_id": conversation_id, "created_at": now}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return _serialize_user(res) if res else None


async def getUserData(col: AsyncIOMotorCollection, conversation_id: str) -> Optional[Dict[str, Any]]:
    doc = await col.find_one({"conversation_id": conversation_id})
    return _serialize_user(doc) if doc else None


async def listUsersData(col: AsyncIOMotorCollection, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
    cursor = col.find({}, sort=[("_id", -1)]).skip(skip).limit(limit)
    return [_serialize_user(doc) async for doc in cursor]


