from fastapi import APIRouter
from app.endpoints.v00 import bridge

router = APIRouter()
router.include_router(bridge.router)