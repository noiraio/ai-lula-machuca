from datetime import datetime, timezone
from typing import Annotated, Any, Optional

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


def oid(value: str, detail: str = "Registro não encontrado") -> ObjectId:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail=detail)


class BaseDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[PyObjectId] = Field(default=None, validation_alias=AliasChoices("_id", "id"))

    @field_validator("*", mode="before")
    @classmethod
    def _normalizar(cls, v: Any) -> Any:
        if isinstance(v, datetime):
            return utc(v)
        return _to_str(v)

    def to_mongo(self) -> dict:
        return self.model_dump(exclude={"id"}, exclude_none=True)

    @classmethod
    def from_mongo(cls, doc: dict | None):
        return cls.model_validate(doc) if doc is not None else None
