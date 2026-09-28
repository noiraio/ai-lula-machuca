from fastapi import APIRouter, Depends

from app import crud
from app.db import db
from app.dependencies import get_current_user
from app.schemas.servico import ServicoCreate, ServicoResponse, ServicoUpdate

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
