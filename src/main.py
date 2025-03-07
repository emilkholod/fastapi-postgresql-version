from typing import Annotated

import asyncpg
import uvicorn
from fastapi import APIRouter, Depends, FastAPI, Request

from lifespan import lifespan


async def get_pg_connection(request: Request) -> asyncpg.Connection:
    async with request.state.db_pool.acquire() as conn:
        yield conn


async def get_db_version(
    conn: Annotated[asyncpg.Connection, Depends(get_pg_connection)],
):
    return await conn.fetchval("SELECT version()")


def register_routes(app: FastAPI):
    router = APIRouter(prefix="/api")
    router.add_api_route(path="/db_version", endpoint=get_db_version)
    app.include_router(router)


def create_app() -> FastAPI:
    app = FastAPI(title="e-Comet", lifespan=lifespan)
    register_routes(app)
    return app


if __name__ == "__main__":
    uvicorn.run("main:create_app", factory=True)
