from fastapi import APIRouter
from app.endpoints import v00

router = APIRouter()
router.include_router(v00.router)