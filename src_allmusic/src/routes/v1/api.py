from fastapi import APIRouter

from .endpoints.parser import router as parser_router
from .endpoints.view import router as view_router

router = APIRouter()

router.include_router(parser_router)
router.include_router(view_router)
