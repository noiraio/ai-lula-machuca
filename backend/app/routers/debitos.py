from fastapi import APIRouter, Depends

from app import crud
from app.db import db
from app.dependencies import get_current_user
from app.schemas.debito import DebitoCreate, DebitoResponse

router = APIRouter(prefix="/debitos", tags=["debitos"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[DebitoResponse])
async def listar():
    return await crud.listar(db.debitos, DebitoResponse, ordem=-1)


@router.post("/", response_model=DebitoResponse, status_code=201)
async def criar(body: DebitoCreate):
    return await crud.criar(db.debitos, DebitoResponse, body, {"salao_id": 1})


@router.delete("/{debito_id}", status_code=204)
async def deletar(debito_id: str):
    await crud.deletar(db.debitos, debito_id, "Débito não encontrado")
