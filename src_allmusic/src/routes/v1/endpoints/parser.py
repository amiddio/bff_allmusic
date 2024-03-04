from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from allmusic.artist_graber import ArtistGraber
from database.database import get_db
from schemas.artist import ArtistsRequest

router = APIRouter(prefix='/parser')


@router.post('', response_description="Allmusic parser", status_code=status.HTTP_200_OK)
async def website_parser(artists: ArtistsRequest, db: Session = Depends(get_db)) -> dict:
    result = await ArtistGraber(db=db).grab(artists=artists)
    return {'response': result}
