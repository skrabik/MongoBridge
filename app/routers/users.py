from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorCollection

from app.db import getUsersCollection
from app.models.record import UserDataCreate, UserDataPatch, UserDataOut
from app.repositories.users import getUserData, upsertUserData, mergeUserData, listUsersData


router = APIRouter()


def usersCollectionDep() -> AsyncIOMotorCollection:
    return getUsersCollection()


@router.get("/users", response_model=list[UserDataOut])
async def listUsersRoute(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    col: AsyncIOMotorCollection = Depends(usersCollectionDep),
):
    return await listUsersData(col, skip=skip, limit=limit)

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


