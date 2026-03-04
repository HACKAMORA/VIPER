from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_database
from .routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
  await init_database()
  yield


app = FastAPI(
  title=f"{settings.app_name} API",
  version="0.1.0",
  lifespan=lifespan,
)

app.include_router(api_router)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
  return {"status": "ok"}


