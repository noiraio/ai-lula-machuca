from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Optional
from zoneinfo import ZoneInfo

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import AliasChoices, BaseModel, BeforeValidator, ConfigDict, Field, field_validator

from app import config

client = AsyncIOMotorClient(config.MONGO_URL)
db = client[config.DB_NAME]


def _to_str(v: Any) -> Any:
    return str(v) if isinstance(v, ObjectId) else v


PyObjectId = Annotated[str, BeforeValidator(_to_str)]


def utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt


def now() -> datetime:
    return datetime.now(timezone.utc)


TZ = ZoneInfo(config.TIMEZONE)


def local(dt: datetime) -> datetime:
    return utc(dt).astimezone(TZ)


def janela_dia(offset_dias: int = 0) -> tuple[datetime, datetime]:
    inicio = now().astimezone(TZ).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=offset_dias)
    return inicio, inicio + timedelta(days=1)


def oid(value: str, detail: str = "Registro não encontrado") -> ObjectId:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail=detail)


class MongoModel(BaseModel):
    """Normaliza ObjectId → str e datetimes naive (UTC) → aware em qualquer nível."""

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("*", mode="before")
    @classmethod
    def _normalizar(cls, v: Any) -> Any:
        if isinstance(v, datetime):
            return utc(v)
        return _to_str(v)


class BaseDocument(MongoModel):
    id: Optional[PyObjectId] = Field(default=None, validation_alias=AliasChoices("_id", "id"))

    def to_mongo(self) -> dict:
        return self.model_dump(exclude={"id"}, exclude_none=True)

    @classmethod
    def from_mongo(cls, doc: dict | None):
        return cls.model_validate(doc) if doc is not None else None
