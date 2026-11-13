
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, JSON
from backend.app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(15), nullable=False)
    opening_time = Column(String(10), nullable=False)
    closing_time = Column(String(10), nullable=False)


class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False
    )
    table_number = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    seating_type = Column(String(30), nullable=False)
    is_available = Column(Boolean, default=True)



class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False
    )
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    is_vegetarian = Column(Boolean, default=False)
    ingredients = Column(JSON, nullable=False)
    dietary_tags = Column(JSON, default=list)
    allergens = Column(JSON, default=dict)
    is_available = Column(Boolean, default=True)
