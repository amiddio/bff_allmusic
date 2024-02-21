from fastapi import APIRouter

router = APIRouter(prefix='/testing')


@router.get('/', response_description="Testing")
async def get_all_artists() -> dict:
    return {"detail": "Hallo, world!"}
