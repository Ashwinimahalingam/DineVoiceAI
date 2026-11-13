
from pydantic import BaseModel, Field
from typing import Literal


class TableCreate(BaseModel):
    restaurant_id: int = Field(gt=0)
    table_number: int = Field(gt=0)
    capacity: int = Field(gt=0, le=20)

    seating_type: Literal[
        "indoor",
        "outdoor",
        "window"
    ]


class TableResponse(BaseModel):
    id: int
    restaurant_id: int
    table_number: int
    capacity: int
    seating_type: str
    is_available: bool

    model_config = {"from_attributes": True}
