from fastapi import APIRouter

from .endpoints.allmusic import router as allmusic_router

router = APIRouter()

router.include_router(allmusic_router)
