from pydantic import BaseModel, Field


class ReleaseTypeDetail(BaseModel):
    """
    Схема детальной информации о типе релиза
    """

    id: int = Field(alias='release_type_id')
    type: str
    name: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "release_type_id": 1,
                "type": "main",
                "name": "Main Albums",
            }
        }
    }

