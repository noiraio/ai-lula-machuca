from fastapi import APIRouter, Depends

from app import crud
from app.db import db, now
from app.dependencies import get_current_user
from app.schemas.financeiro import MovimentoCreate, MovimentoResponse, ResumoFinanceiroResponse

router = APIRouter(prefix="/financeiro", tags=["financeiro"], dependencies=[Depends(get_current_user)])


@router.get("/resumo", response_model=ResumoFinanceiroResponse)
async def resumo():
    docs = await db.movimentos_financeiros.find().sort("data", -1).to_list(1000)
    entradas = sum(m["valor"] for m in docs if m["tipo"] == "entrada")
    saidas = sum(m["valor"] for m in docs if m["tipo"] == "saida")
    return ResumoFinanceiroResponse(
        entradas=entradas,
        saidas=saidas,
        saldo=entradas - saidas,
        lancamentos=[MovimentoResponse.from_mongo(m) for m in docs],
    )


@router.post("/lancamentos", response_model=MovimentoResponse, status_code=201)
async def criar_lancamento(body: MovimentoCreate):
    return await crud.criar(db.movimentos_financeiros, MovimentoResponse, body, {"data": now(), "salao_id": 1})
