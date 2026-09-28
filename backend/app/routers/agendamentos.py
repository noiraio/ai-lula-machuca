from datetime import datetime, timedelta

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo import ReturnDocument

from app.db import db, oid
from app.dependencies import get_current_user
from app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse, AgendamentoUpdate

router = APIRouter(prefix="/agendamentos", tags=["agendamentos"], dependencies=[Depends(get_current_user)])
NAO_ENCONTRADO = "Agendamento não encontrado"


async def _mapa(col, ids: list[ObjectId]) -> dict:
    return {d["_id"]: d for d in await col.find({"_id": {"$in": ids}}).to_list(len(ids) or 1)} if ids else {}


async def _responses(docs: list[dict], alertas: list[str] | None = None) -> list[AgendamentoResponse]:
    servicos = await _mapa(db.servicos, [d["servico_id"] for d in docs])
    clientes = await _mapa(db.clientes, [d["cliente_id"] for d in docs])
    profs = await _mapa(db.profissionais, [d["profissional_id"] for d in docs])
    out = []
    for d in docs:
        srv = servicos.get(d["servico_id"], {})
        out.append(
            AgendamentoResponse.from_mongo(
                {
                    **d,
                    "servico_nome": srv.get("nome", "—"),
                    "servico_valor": srv.get("valor", 0.0),
                    "cliente_nome": clientes.get(d["cliente_id"], {}).get("nome"),
                    "profissional_nome": profs.get(d["profissional_id"], {}).get("nome", "—"),
                    "alertas_estoque": alertas or [],
                }
            )
        )
    return out


async def _obter_doc(agendamento_id: str) -> dict:
    doc = await db.agendamentos.find_one({"_id": oid(agendamento_id, NAO_ENCONTRADO)})
    if doc is None:
        raise HTTPException(status_code=404, detail=NAO_ENCONTRADO)
    return doc


async def _exigir(col, item_id: str, detail: str) -> dict:
    doc = await col.find_one({"_id": oid(item_id, detail)})
    if doc is None:
        raise HTTPException(status_code=404, detail=detail)
    return doc


async def _resolver_cliente(body: AgendamentoCreate) -> dict:
    if body.cliente_id:
        return await _exigir(db.clientes, body.cliente_id, "Cliente não encontrado")
    telefone = body.cliente_telefone.strip()
    cliente = await db.clientes.find_one({"telefone": telefone})
    if cliente:
        if body.cliente_nome and not cliente.get("nome"):
            await db.clientes.update_one({"_id": cliente["_id"]}, {"$set": {"nome": body.cliente_nome}})
        return cliente
    novo = {"telefone": telefone, "nome": body.cliente_nome}
    res = await db.clientes.insert_one(novo)
    return {**novo, "_id": res.inserted_id}


async def _checar_conflito(profissional_id: ObjectId, inicio: datetime, fim: datetime, ignorar: ObjectId | None = None):
    filtro = {"profissional_id": profissional_id, "data_hora_inicio": {"$lt": fim}, "data_hora_fim": {"$gt": inicio}}
    if ignorar is not None:
        filtro["_id"] = {"$ne": ignorar}
    if await db.agendamentos.find_one(filtro):
        raise HTTPException(status_code=409, detail="Já existe um agendamento neste horário")


@router.get("/", response_model=list[AgendamentoResponse])
async def listar(
    profissional_id: str | None = Query(None),
    data_inicio: str | None = Query(None),
    data_fim: str | None = Query(None),
):
    filtro: dict = {}
    if profissional_id:
        filtro["profissional_id"] = oid(profissional_id, "Profissional não encontrado")
    periodo = {}
    if data_inicio:
        periodo["$gte"] = datetime.fromisoformat(data_inicio)
    if data_fim:
        periodo["$lt"] = datetime.fromisoformat(data_fim)
    if periodo:
        filtro["data_hora_inicio"] = periodo
    docs = await db.agendamentos.find(filtro).sort("data_hora_inicio", 1).to_list(500)
    return await _responses(docs)


@router.post("/", response_model=AgendamentoResponse, status_code=201)
async def criar(body: AgendamentoCreate):
    servico = await _exigir(db.servicos, body.servico_id, "Serviço não encontrado")
    profissional = await _exigir(db.profissionais, body.profissional_id, "Profissional não encontrado")
    cliente = await _resolver_cliente(body)

    inicio = body.data_hora_inicio
    fim = body.data_hora_fim or (inicio + timedelta(minutes=servico["duracao_minutos"]))
    await _checar_conflito(profissional["_id"], inicio, fim)

    doc = {
        "cliente_id": cliente["_id"],
        "profissional_id": profissional["_id"],
        "servico_id": servico["_id"],
        "data_hora_inicio": inicio,
        "data_hora_fim": fim,
        "status": "confirmado",
        "salao_id": 1,
    }
    res = await db.agendamentos.insert_one(doc)
    return (await _responses([{**doc, "_id": res.inserted_id}]))[0]


async def _deduzir_insumos(servico_id: ObjectId) -> list[str]:
    relacoes = await db.servico_insumos.find({"servico_id": servico_id}).to_list(100)
    alertas: list[str] = []
    for rel in relacoes:
        insumo = await db.insumos.find_one({"_id": rel["insumo_id"]})
        if insumo is None:
            continue
        nova_qtd = insumo["quantidade_atual"] - rel["quantidade_utilizada"]
        if nova_qtd < 0:
            raise HTTPException(
                status_code=409,
                detail=f"Estoque insuficiente para '{insumo['nome']}': tem {insumo['quantidade_atual']}, precisa de {rel['quantidade_utilizada']}",
            )
        await db.insumos.update_one({"_id": insumo["_id"]}, {"$set": {"quantidade_atual": nova_qtd}})
        if nova_qtd <= insumo["quantidade_minima_alerta"]:
            alertas.append(f"{insumo['nome']} está com estoque baixo ({nova_qtd} un)")
    return alertas


@router.patch("/{agendamento_id}/concluir", response_model=AgendamentoResponse)
async def concluir(agendamento_id: str):
    doc = await _obter_doc(agendamento_id)
    alertas = await _deduzir_insumos(doc["servico_id"]) if doc["status"] != "concluido" else []
    doc = await db.agendamentos.find_one_and_update(
        {"_id": doc["_id"]}, {"$set": {"status": "concluido"}}, return_document=ReturnDocument.AFTER
    )
    return (await _responses([doc], alertas))[0]


@router.put("/{agendamento_id}", response_model=AgendamentoResponse)
async def atualizar(agendamento_id: str, body: AgendamentoUpdate):
    atual = await _obter_doc(agendamento_id)
    campos: dict = {}
    if body.servico_id is not None:
        campos["servico_id"] = (await _exigir(db.servicos, body.servico_id, "Serviço não encontrado"))["_id"]
    if body.profissional_id is not None:
        campos["profissional_id"] = (await _exigir(db.profissionais, body.profissional_id, "Profissional não encontrado"))["_id"]
    if body.cliente_id is not None:
        campos["cliente_id"] = (await _exigir(db.clientes, body.cliente_id, "Cliente não encontrado"))["_id"]
    for campo in ("data_hora_inicio", "data_hora_fim", "status"):
        valor = getattr(body, campo)
        if valor is not None:
            campos[campo] = valor

    if "data_hora_inicio" in campos or "data_hora_fim" in campos or "profissional_id" in campos:
        await _checar_conflito(
            campos.get("profissional_id", atual["profissional_id"]),
            campos.get("data_hora_inicio", atual["data_hora_inicio"]),
            campos.get("data_hora_fim", atual["data_hora_fim"]),
            ignorar=atual["_id"],
        )

    if campos:
        atual = await db.agendamentos.find_one_and_update(
            {"_id": atual["_id"]}, {"$set": campos}, return_document=ReturnDocument.AFTER
        )
    return (await _responses([atual]))[0]


@router.delete("/{agendamento_id}", status_code=204)
async def deletar(agendamento_id: str):
    res = await db.agendamentos.delete_one({"_id": oid(agendamento_id, NAO_ENCONTRADO)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail=NAO_ENCONTRADO)
