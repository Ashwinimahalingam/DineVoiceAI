
from pydantic import BaseModel, Field
from typing import Literal


DietaryTag = Literal[
    "vegetarian",
    "vegan",
    "jain",
    "gluten_free",
    "dairy_free"
]

AllergenStatus = Literal[
    "contains",
    "may_contain",
    "cross_contact_possible",
    "unknown"
]


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    description: str = Field(min_length=5)

    price: float = Field(gt=0)

    category: Literal[
        "starter",
        "main_course",
        "dessert",
        "beverage"
    ]

    is_vegetarian: bool

    ingredients: list[str] = Field(min_length=1)

    dietary_tags: list[DietaryTag] = Field(
        default_factory=list
    )

    allergens: dict[str, AllergenStatus] = Field(
        default_factory=dict
    )


class MenuItemResponse(BaseModel):
    id: int

    name: str

    description: str

    price: float

    category: str

    is_vegetarian: bool

    ingredients: list[str]

    dietary_tags: list[str]

    allergens: dict[str, str]

    is_available: bool
