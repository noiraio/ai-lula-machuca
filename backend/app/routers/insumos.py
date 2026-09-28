from fastapi import APIRouter, Depends

from app import crud
from app.db import db, oid
from app.dependencies import get_current_user
from app.schemas.insumo import InsumoCreate, InsumoResponse, InsumoUpdate

router = APIRouter(prefix="/insumos", tags=["insumos"], dependencies=[Depends(get_current_user)])
NAO_ENCONTRADO = "Insumo não encontrado"


@router.get("/", response_model=list[InsumoResponse])
async def listar():
    return await crud.listar(db.insumos, InsumoResponse)


@router.post("/", response_model=InsumoResponse, status_code=201)
async def criar(body: InsumoCreate):
    return await crud.criar(db.insumos, InsumoResponse, body, {"salao_id": 1})


@router.get("/{insumo_id}", response_model=InsumoResponse)
async def obter(insumo_id: str):
    return await crud.obter(db.insumos, InsumoResponse, insumo_id, NAO_ENCONTRADO)


@router.put("/{insumo_id}", response_model=InsumoResponse)
async def atualizar(insumo_id: str, body: InsumoUpdate):
    return await crud.atualizar(db.insumos, InsumoResponse, insumo_id, body, NAO_ENCONTRADO)


@router.delete("/{insumo_id}", status_code=204)
async def deletar(insumo_id: str):
    await crud.deletar(db.insumos, insumo_id, NAO_ENCONTRADO)
    await db.servico_insumos.delete_many({"insumo_id": oid(insumo_id)})
