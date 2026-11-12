from backend.app.schemas.menu import MenuItemCreate, MenuItemResponse
from backend.app.schemas.table import TableCreate, TableResponse
from fastapi import FastAPI, HTTPException
from backend.app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse
)

app = FastAPI(
    title="DineVoice AI",
    description="AI-powered restaurant voice receptionist",
    version="0.2.0"
)

# Temporary storage (we will replace this with PostgreSQL)
restaurants = []
next_restaurant_id = 1


@app.get("/")
def home():
    return {
        "message": "Welcome to DineVoice AI!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "DineVoice AI"
    }


@app.post("/restaurants", response_model=RestaurantResponse)
def create_restaurant(restaurant: RestaurantCreate):
    global next_restaurant_id

    new_restaurant = {
        "id": next_restaurant_id,
        **restaurant.model_dump()
    }

    restaurants.append(new_restaurant)
    next_restaurant_id += 1

    return new_restaurant


@app.get("/restaurants", response_model=list[RestaurantResponse])
def get_restaurants():
    return restaurants


@app.get("/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int):
    for restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            return restaurant

    raise HTTPException(
        status_code=404,
        detail="Restaurant not found"
    )

# Temporary table storage
tables = []
next_table_id = 1


@app.post("/tables", response_model=TableResponse)
def create_table(table: TableCreate):
    global next_table_id

    new_table = {
        "id": next_table_id,
        **table.model_dump(),
        "is_available": True
    }

    tables.append(new_table)
    next_table_id += 1

    return new_table


@app.get("/tables", response_model=list[TableResponse])
def get_tables():
    return tables


@app.get("/tables/{table_id}", response_model=TableResponse)
def get_table(table_id: int):
    for table in tables:
        if table["id"] == table_id:
            return table

    raise HTTPException(
        status_code=404,
        detail="Table not found"
    )

# Temporary menu storage
menu_items = []
next_menu_id = 1


# Create a menu item
@app.post("/menu", response_model=MenuItemResponse)
def create_menu_item(item: MenuItemCreate):
    global next_menu_id

    new_item = {
        "id": next_menu_id,
        **item.model_dump(),
        "is_available": True
    }

    menu_items.append(new_item)
    next_menu_id += 1

    return new_item


# Get all menu items
@app.get("/menu", response_model=list[MenuItemResponse])
def get_menu_items():
    return menu_items


# Search menu items
@app.get("/menu/search", response_model=list[MenuItemResponse])
def search_menu_items(q: str):
    results = [
        item for item in menu_items
        if q.lower() in item["name"].lower()
        or q.lower() in item["description"].lower()
    ]

    return results


# Get menu item by ID
@app.get("/menu/{item_id}", response_model=MenuItemResponse)
def get_menu_item(item_id: int):
    for item in menu_items:
        if item["id"] == item_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Menu item not found"
    )


