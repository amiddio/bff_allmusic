from pydantic import BaseModel


class TrackDetail(BaseModel):
    num: str
    title: str
    composers: str
    performers: str
    duration: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "num": "7",
                "title": "No Quarter",
                "composers": "John Paul Jones / Jimmy Page / Robert Plant",
                "performers": "Led Zeppelin",
                "duration": "07:02",
            }
        }
    }


class Disc(BaseModel):
    label: str
    items: list[TrackDetail]

    model_config = {
        "json_schema_extra": {
            "example": {
                "label": "Disc 1",
            }
        }
    }
