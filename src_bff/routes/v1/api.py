from fastapi import APIRouter

from endpoints.testing import router as testing_router

router = APIRouter()

router.include_router(testing_router)
