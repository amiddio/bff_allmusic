from fastapi import APIRouter

from .endpoints.allmusic import router as allmusic_router
from .endpoints.user import router as user_router

router = APIRouter()

router.include_router(allmusic_router)
router.include_router(user_router)
