from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument


def _serialize(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(doc.get("_id")),
        "payload": doc.get("payload", {}),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }


async def createRecord(col: AsyncIOMotorCollection, payload: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    doc = {"payload": payload, "created_at": now, "updated_at": now}
    result = await col.insert_one(doc)
    inserted = await col.find_one({"_id": result.inserted_id})
    return _serialize(inserted)


async def getRecord(col: AsyncIOMotorCollection, record_id: str) -> Optional[Dict[str, Any]]:
    doc = await col.find_one({"_id": ObjectId(record_id)})
    return _serialize(doc) if doc else None


async def listRecords(col: AsyncIOMotorCollection, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
    cursor = col.find({}, sort=[("_id", -1)]).skip(skip).limit(limit)
    return [_serialize(doc) async for doc in cursor]


async def updateRecord(col: AsyncIOMotorCollection, record_id: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    res = await col.find_one_and_update(
        {"_id": ObjectId(record_id)},
        {"$set": {"payload": payload, "updated_at": now}},
        return_document=ReturnDocument.AFTER,
    )
    return _serialize(res) if res else None


async def deleteRecord(col: AsyncIOMotorCollection, record_id: str) -> bool:
    res = await col.delete_one({"_id": ObjectId(record_id)})
    return res.deleted_count == 1


async def addToRecordPayload(col: AsyncIOMotorCollection, record_id: str, payload_patch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    # Сливаем словари на верхнем уровне: существующий payload ∪ payload_patch
    # Используем оператор $set для поэлементного обновления ключей payload.
    set_update: Dict[str, Any] = {f"payload.{k}": v for k, v in payload_patch.items()}
    set_update["updated_at"] = now
    res = await col.find_one_and_update(
        {"_id": ObjectId(record_id)},
        {"$set": set_update},
        return_document=ReturnDocument.AFTER,
    )
    return _serialize(res) if res else None
