from datetime import timedelta

from fastapi import APIRouter, Depends

from app.db import db, now
from app.dependencies import get_current_user
from app.schemas.estoque import AlertaEstoqueResponse

router = APIRouter(prefix="/estoque", tags=["estoque"], dependencies=[Depends(get_current_user)])


async def _demanda_proximos_dias(dias: int = 7) -> dict:
    agora = now()
    pipeline = [
        {"$match": {"status": "confirmado", "data_hora_inicio": {"$gte": agora, "$lt": agora + timedelta(days=dias)}}},
        {"$group": {"_id": "$servico_id", "total": {"$sum": 1}}},
    ]
    counts = {r["_id"]: r["total"] async for r in db.agendamentos.aggregate(pipeline)}
    if not counts:
        return {}
    demanda: dict = {}
    async for rel in db.servico_insumos.find({"servico_id": {"$in": list(counts)}}):
        demanda[rel["insumo_id"]] = demanda.get(rel["insumo_id"], 0) + rel["quantidade_utilizada"] * counts[rel["servico_id"]]
    return demanda


@router.get("/alertas", response_model=list[AlertaEstoqueResponse])
async def alertas_estoque():
    demanda = await _demanda_proximos_dias()
    insumos = {i["_id"]: i for i in await db.insumos.find().to_list(500)}
    alertas: list[AlertaEstoqueResponse] = []

    for insumo_id, necessario in demanda.items():
        insumo = insumos.get(insumo_id)
        if insumo and insumo["quantidade_atual"] < necessario:
            alertas.append(
                AlertaEstoqueResponse(
                    insumo_id=str(insumo_id),
                    nome=insumo["nome"],
                    quantidade_atual=insumo["quantidade_atual"],
                    quantidade_minima_alerta=insumo["quantidade_minima_alerta"],
                    demanda_prevista=round(necessario, 1),
                    tipo="demanda",
                    mensagem=f"Reposição necessária: {insumo['nome']} (tem {insumo['quantidade_atual']}, precisa de {necessario:.0f})",
                )
            )

    com_alerta = {a.insumo_id for a in alertas}
    for insumo in insumos.values():
        if str(insumo["_id"]) in com_alerta or insumo["quantidade_atual"] > insumo["quantidade_minima_alerta"]:
            continue
        alertas.append(
            AlertaEstoqueResponse(
                insumo_id=str(insumo["_id"]),
                nome=insumo["nome"],
                quantidade_atual=insumo["quantidade_atual"],
                quantidade_minima_alerta=insumo["quantidade_minima_alerta"],
                demanda_prevista=0,
                tipo="minimo",
                mensagem=f"Estoque baixo: {insumo['nome']} ({insumo['quantidade_atual']}/{insumo['quantidade_minima_alerta']} mín.)",
            )
        )
    return alertas
