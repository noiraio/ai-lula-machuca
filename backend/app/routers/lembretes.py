from fastapi import APIRouter, Depends

from app import crud
from app.db import db, now
from app.dependencies import get_current_user
from app.schemas.lembrete import LembreteCreate, LembreteResponse

router = APIRouter(prefix="/lembretes", tags=["lembretes"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[LembreteResponse])
async def listar():
    return await crud.listar(db.lembretes, LembreteResponse, ordem=-1)


@router.post("/", response_model=LembreteResponse, status_code=201)
async def criar(body: LembreteCreate):
    return await crud.criar(db.lembretes, LembreteResponse, body, {"criado_em": now(), "salao_id": 1})
