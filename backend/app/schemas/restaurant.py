
from pydantic import BaseModel, Field


class RestaurantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    address: str = Field(min_length=5)
    phone_number: str = Field(min_length=10, max_length=15)
    opening_time: str
    closing_time: str


class RestaurantResponse(BaseModel):
    id: int
    name: str
    address: str
    phone_number: str
    opening_time: str
    closing_time: str
