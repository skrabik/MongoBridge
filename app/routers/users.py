from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from app.db import getUsersCollection
from app.models.record import UserDataCreate, UserDataPatch, UserDataOut
from app.repositories.users import getUserData, upsertUserData, mergeUserData


router = APIRouter()


def usersCollectionDep() -> AsyncIOMotorCollection:
    return getUsersCollection()


@router.get("/users/{conversation_id}", response_model=UserDataOut)
async def getUserRoute(conversation_id: str, col: AsyncIOMotorCollection = Depends(usersCollectionDep)):
    doc = await getUserData(col, conversation_id)
    if not doc:
        raise HTTPException(status_code=404, detail="User data not found")
    return doc


@router.put("/users/{conversation_id}", response_model=UserDataOut)
async def putUserRoute(conversation_id: str, body: UserDataCreate, col: AsyncIOMotorCollection = Depends(usersCollectionDep)):
    if body.conversation_id != conversation_id:
        raise HTTPException(status_code=400, detail="conversation_id mismatch")
    return await upsertUserData(col, conversation_id, body.data)


@router.patch("/users/{conversation_id}", response_model=UserDataOut)
async def patchUserRoute(conversation_id: str, body: UserDataPatch, col: AsyncIOMotorCollection = Depends(usersCollectionDep)):
    doc = await mergeUserData(col, conversation_id, body.data)
    if not doc:
        raise HTTPException(status_code=404, detail="User data not found")
    return doc


