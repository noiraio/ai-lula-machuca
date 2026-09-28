from fastapi import APIRouter, Depends

from app import crud
from app.db import db
from app.dependencies import get_current_user
from app.schemas.profissional import ProfissionalCreate, ProfissionalResponse, ProfissionalUpdate

router = APIRouter(prefix="/profissionais", tags=["profissionais"], dependencies=[Depends(get_current_user)])
NAO_ENCONTRADO = "Profissional não encontrado"


@router.get("/", response_model=list[ProfissionalResponse])
async def listar():
    return await crud.listar(db.profissionais, ProfissionalResponse)


@router.post("/", response_model=ProfissionalResponse, status_code=201)
async def criar(body: ProfissionalCreate):
    return await crud.criar(db.profissionais, ProfissionalResponse, body, {"salao_id": 1})


@router.get("/{profissional_id}", response_model=ProfissionalResponse)
async def obter(profissional_id: str):
    return await crud.obter(db.profissionais, ProfissionalResponse, profissional_id, NAO_ENCONTRADO)


@router.put("/{profissional_id}", response_model=ProfissionalResponse)
async def atualizar(profissional_id: str, body: ProfissionalUpdate):
    return await crud.atualizar(db.profissionais, ProfissionalResponse, profissional_id, body, NAO_ENCONTRADO)


@router.delete("/{profissional_id}", status_code=204)
async def deletar(profissional_id: str):
    await crud.deletar(db.profissionais, profissional_id, NAO_ENCONTRADO)
