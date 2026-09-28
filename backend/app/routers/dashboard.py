from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query

from app.db import db
from app.dependencies import get_current_user
from app.schemas.financeiro import FaturamentoResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"], dependencies=[Depends(get_current_user)])


@router.get("/financeiro", response_model=FaturamentoResponse)
async def financeiro(data_inicio: str = Query(...), data_fim: str = Query(...)):
    dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    dt_fim = datetime.strptime(data_fim, "%Y-%m-%d").replace(tzinfo=timezone.utc) + timedelta(days=1)

    concluidos = await db.agendamentos.find(
        {"status": "concluido", "data_hora_inicio": {"$gte": dt_inicio, "$lt": dt_fim}}
    ).to_list(5000)
    ids = list({a["servico_id"] for a in concluidos})
    valores = {s["_id"]: s["valor"] for s in await db.servicos.find({"_id": {"$in": ids}}).to_list(len(ids) or 1)} if ids else {}
    total = sum(valores.get(a["servico_id"], 0.0) for a in concluidos)
    return FaturamentoResponse(total=total, data_inicio=data_inicio, data_fim=data_fim)
