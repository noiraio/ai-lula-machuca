from fastapi import APIRouter, Depends, HTTPException
from pymongo import ReturnDocument

from app import crud
from app.db import db, oid
from app.dependencies import get_current_user
from app.schemas.servico import (
    ServicoCreate,
    ServicoInsumoCreate,
    ServicoInsumoResponse,
    ServicoResponse,
    ServicoUpdate,
)

router = APIRouter(prefix="/servicos", tags=["servicos"], dependencies=[Depends(get_current_user)])
NAO_ENCONTRADO = "Serviço não encontrado"


@router.get("/", response_model=list[ServicoResponse])
async def listar():
    return await crud.listar(db.servicos, ServicoResponse)


@router.post("/", response_model=ServicoResponse, status_code=201)
async def criar(body: ServicoCreate):
    return await crud.criar(db.servicos, ServicoResponse, body, {"salao_id": 1})


@router.get("/{servico_id}", response_model=ServicoResponse)
async def obter(servico_id: str):
    return await crud.obter(db.servicos, ServicoResponse, servico_id, NAO_ENCONTRADO)


@router.put("/{servico_id}", response_model=ServicoResponse)
async def atualizar(servico_id: str, body: ServicoUpdate):
    return await crud.atualizar(db.servicos, ServicoResponse, servico_id, body, NAO_ENCONTRADO)


@router.delete("/{servico_id}", status_code=204)
async def deletar(servico_id: str):
    await crud.deletar(db.servicos, servico_id, NAO_ENCONTRADO)
    await db.servico_insumos.delete_many({"servico_id": oid(servico_id)})


# ---------- Insumos consumidos por serviço ----------


async def _relacoes(servico_id) -> list[ServicoInsumoResponse]:
    rels = await db.servico_insumos.find({"servico_id": servico_id}).to_list(200)
    ids = [r["insumo_id"] for r in rels]
    insumos = {i["_id"]: i for i in await db.insumos.find({"_id": {"$in": ids}}).to_list(len(ids) or 1)} if ids else {}
    out = []
    for r in rels:
        ins = insumos.get(r["insumo_id"], {})
        out.append(
            ServicoInsumoResponse.from_mongo(
                {
                    **r,
                    "insumo_nome": ins.get("nome", "—"),
                    "quantidade_atual": ins.get("quantidade_atual", 0),
                    "quantidade_minima_alerta": ins.get("quantidade_minima_alerta", 0),
                }
            )
        )
    return sorted(out, key=lambda x: x.insumo_nome)


@router.get("/{servico_id}/insumos", response_model=list[ServicoInsumoResponse])
async def listar_insumos(servico_id: str):
    await crud.obter(db.servicos, ServicoResponse, servico_id, NAO_ENCONTRADO)
    return await _relacoes(oid(servico_id))


@router.post("/{servico_id}/insumos", response_model=list[ServicoInsumoResponse], status_code=201)
async def vincular_insumo(servico_id: str, body: ServicoInsumoCreate):
    """Cria ou atualiza a quantidade consumida do insumo neste serviço."""
    await crud.obter(db.servicos, ServicoResponse, servico_id, NAO_ENCONTRADO)
    insumo_oid = oid(body.insumo_id, "Insumo não encontrado")
    if await db.insumos.find_one({"_id": insumo_oid}) is None:
        raise HTTPException(status_code=404, detail="Insumo não encontrado")
    await db.servico_insumos.find_one_and_update(
        {"servico_id": oid(servico_id), "insumo_id": insumo_oid},
        {"$set": {"quantidade_utilizada": body.quantidade_utilizada}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return await _relacoes(oid(servico_id))


@router.delete("/{servico_id}/insumos/{insumo_id}", status_code=204)
async def desvincular_insumo(servico_id: str, insumo_id: str):
    res = await db.servico_insumos.delete_one({"servico_id": oid(servico_id), "insumo_id": oid(insumo_id, "Insumo não encontrado")})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Vínculo não encontrado")
