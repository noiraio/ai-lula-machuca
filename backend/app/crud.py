from fastapi import HTTPException
from pydantic import BaseModel
from pymongo import ReturnDocument

from app.db import oid


async def listar(col, model, ordem: int = 1) -> list:
    return [model.from_mongo(d) async for d in col.find().sort("_id", ordem)]


async def criar(col, model, body: BaseModel, extra: dict | None = None):
    doc = {**body.model_dump(), **(extra or {})}
    res = await col.insert_one(doc)
    return model.from_mongo({**doc, "_id": res.inserted_id})


async def obter(col, model, item_id: str, nao_encontrado: str):
    doc = await col.find_one({"_id": oid(item_id, nao_encontrado)})
    if doc is None:
        raise HTTPException(status_code=404, detail=nao_encontrado)
    return model.from_mongo(doc)


async def atualizar(col, model, item_id: str, body: BaseModel, nao_encontrado: str):
    campos = body.model_dump(exclude_unset=True, exclude_none=True)
    if not campos:
        return await obter(col, model, item_id, nao_encontrado)
    doc = await col.find_one_and_update(
        {"_id": oid(item_id, nao_encontrado)}, {"$set": campos}, return_document=ReturnDocument.AFTER
    )
    if doc is None:
        raise HTTPException(status_code=404, detail=nao_encontrado)
    return model.from_mongo(doc)


async def deletar(col, item_id: str, nao_encontrado: str) -> None:
    res = await col.delete_one({"_id": oid(item_id, nao_encontrado)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail=nao_encontrado)
