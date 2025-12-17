import os

import psutil
from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import auth_backend
from src.auth.models import User, user
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.auth.manager import get_user_manager
from src.database import get_async_session
from src.scheduler.scheduler import scheduler
from src.teams.router import router as teams_router
from src.games.router import router as games_router
from src.fill_default import router as fill_default_router

import time

from fastapi import Request

from src.metrics import (
    REQUESTS_TOTAL,
    REQUESTS_ERRORS,
    REQUESTS_DURATION,
    CPU_PERCENT,
    MEMORY_RSS,
    MEMORY_PERCENT,
)

from fastapi import Response

app = FastAPI(
    title="Запись на игру",
    version="0.1",
)


origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://0.0.0.0:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def prometheus_metrics_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        status = response.status_code
        REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=request.url.path,
            status=status,
        ).inc()

        if status >= 400:
            REQUESTS_ERRORS.labels(
                method=request.method,
                endpoint=request.url.path,
                status=status,
            ).inc()

        REQUESTS_DURATION.labels(
            method=request.method,
            endpoint=request.url.path,
        ).set(duration)

        return response

    except Exception:
        duration = time.time() - start_time
        REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=request.url.path,
            status=500,
        ).inc()
        REQUESTS_ERRORS.labels(
            method=request.method,
            endpoint=request.url.path,
            status=500,
        ).inc()
        REQUESTS_DURATION.labels(method=request.method, endpoint=request.url.path).set(
            duration
        )


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)


@app.get("/user/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        this_user = dict(result.mappings().one())
        return {
            "status": "success",
            "data": this_user,
            "details": None,
        }
    except Exception as e:
        return {"status": "error", "data": None, "details": str(e)}


current_process = psutil.Process(os.getpid())


@app.get("/metrics")
def metrics():
    CPU_PERCENT.set(current_process.cpu_percent())
    MEMORY_RSS.set(current_process.memory_info().rss)
    MEMORY_PERCENT.set(current_process.memory_percent())

    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.include_router(teams_router)
app.include_router(games_router)
app.include_router(fill_default_router)


@app.on_event("startup")
async def startup():
    scheduler.start()
    print("Scheduler started")
