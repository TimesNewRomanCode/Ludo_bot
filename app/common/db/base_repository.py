from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Result, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.common.db.core_model import CoreModel

ModelType = TypeVar("ModelType", bound=CoreModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_one(
        self,
        db: AsyncSession,
        sid: Any,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> ModelType | None:
        query = select(self.model).where(self.model.sid == sid)

        if custom_options is not None:
            query = query.options(*custom_options)

        result: Result = await db.execute(query)
        return result.scalars().first()

    async def get_all(
        self,
        db: AsyncSession,
        custom_options: tuple[ExecutableOption, ...] | None = None,
        filter_criteria: Any = None,
    ) -> Sequence[ModelType]:
        query = select(self.model)

        if filter_criteria is not None:
            query = query.where(filter_criteria)
        if custom_options is not None:
            query = query.options(*custom_options)

        result: Result = await db.execute(query)
        return result.scalars().all()

    async def get_all_paginated(
        self,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> Sequence[ModelType]:
        query = select(self.model).offset(offset).limit(limit)

        if custom_options is not None:
            query = query.options(*custom_options)

        result: Result = await db.execute(query)
        return result.scalars().all()

    async def create(
        self, db: AsyncSession, obj_in: CreateSchemaType, with_commit: bool = True
    ) -> ModelType:
        try:
            db_obj = self.model(**obj_in.model_dump())
            db.add(db_obj)

            if with_commit:
                await db.commit()
                await db.refresh(db_obj)
            else:
                await db.flush()

            return db_obj
        except IntegrityError as e:
            raise IntegrityError from e

    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        pass

    async def delete(
        self, db: AsyncSession, sid: Any, with_commit: bool = True
    ) -> ModelType | None:
        query = select(self.model).where(self.model.sid == sid)
        result: Result = await db.execute(query)
        obj = result.scalars().first()
        if obj:
            await db.delete(obj)

            if with_commit:
                await db.commit()
            else:
                await db.flush()

        return obj

    async def get_multi(
        self,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> Sequence[ModelType]:
        query = select(self.model).offset(offset).limit(limit)

        if custom_options is not None:
            query = query.options(*custom_options)

        result: Result = await db.execute(query)
        return result.scalars().all()
