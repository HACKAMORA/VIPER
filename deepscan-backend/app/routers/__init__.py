# app/routers/__init__.py
from fastapi import APIRouter
from .discovery import router

api_router = APIRouter()
api_router.include_router(router)