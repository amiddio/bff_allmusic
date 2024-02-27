from fastapi import APIRouter

from .endpoints.user import router as user_router
from .endpoints.subscribe import router as subscribe_router

router = APIRouter()

router.include_router(user_router)
router.include_router(subscribe_router)
