from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorCollection

from app.db import getCollection
from app.models.record import RecordCreate, RecordUpdate, RecordOut, RecordPayloadAdd
from app.repositories.records import (
    createRecord,
    getRecord,
    listRecords,
    updateRecord,
    deleteRecord,
    addToRecordPayload,
)


router = APIRouter()


def collectionDep() -> AsyncIOMotorCollection:
    return getCollection()


@router.post("/records", response_model=RecordOut)
async def createRecordRoute(body: RecordCreate, col: AsyncIOMotorCollection = Depends(collectionDep)):
    return await createRecord(col, body.payload)


@router.get("/records/{record_id}", response_model=RecordOut)
async def getRecordRoute(record_id: str, col: AsyncIOMotorCollection = Depends(collectionDep)):
    rec = await getRecord(col, record_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    return rec


@router.get("/records", response_model=List[RecordOut])
async def listRecordsRoute(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    col: AsyncIOMotorCollection = Depends(collectionDep),
):
    return await listRecords(col, skip=skip, limit=limit)


@router.patch("/records/{record_id}", response_model=RecordOut)
async def updateRecordRoute(record_id: str, body: RecordUpdate, col: AsyncIOMotorCollection = Depends(collectionDep)):
    payload = body.payload if body.payload is not None else {}
    rec = await updateRecord(col, record_id, payload)
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    return rec


@router.delete("/records/{record_id}")
async def deleteRecordRoute(record_id: str, col: AsyncIOMotorCollection = Depends(collectionDep)):
    ok = await deleteRecord(col, record_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"status": "deleted"}


@router.patch("/records/{record_id}/payload", response_model=RecordOut)
async def addToPayloadRoute(record_id: str, body: RecordPayloadAdd, col: AsyncIOMotorCollection = Depends(collectionDep)):
    rec = await addToRecordPayload(col, record_id, body.payload)
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    return rec

