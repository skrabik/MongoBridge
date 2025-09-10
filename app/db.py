from __future__ import annotations

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from app.settings import getSettings


_client: Optional[AsyncIOMotorClient] = None


def getClient() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        settings = getSettings()
        _client = AsyncIOMotorClient(settings.mongodb_uri)
    return _client


def getDatabase() -> AsyncIOMotorDatabase:
    settings = getSettings()
    return getClient()[settings.mongodb_db]

def getUsersCollection() -> AsyncIOMotorCollection:
    settings = getSettings()
    return getDatabase()[settings.mongodb_users_collection]
