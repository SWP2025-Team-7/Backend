import pytest
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

import os

from backend.main import app
from backend.db.base import metadata

load_dotenv(".env.test")

DATABASE_URL = os.getenv("DATABASE_URL")

engine_test = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    yield

@pytest.fixture(scope="function")
async def client(prepare_database):
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
