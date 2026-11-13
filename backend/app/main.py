
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Restaurant,RestaurantTable,MenuItem

from backend.app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
)

from backend.app.schemas.table import (
    TableCreate,
    TableResponse,
)

from backend.app.schemas.menu import (
    MenuItemCreate,
    MenuItemResponse,
)


app = FastAPI(
    title="DineVoice AI",
    description="AI-powered restaurant voice receptionist",
    version="0.2.0",
)


# --------------------------------
# TEMPORARY STORAGE
# Tables and menu will be migrated
# to PostgreSQL in upcoming steps.
# --------------------------------


# --------------------------------
# TABLE APIs - POSTGRESQL
# --------------------------------

@app.post("/tables", response_model=TableResponse)
def create_table(
    table: TableCreate,
    db: Session = Depends(get_db),
):
    # Check whether the restaurant exists
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == table.restaurant_id)
        .first()
    )

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    # Prevent duplicate table numbers within one restaurant
    existing_table = (
        db.query(RestaurantTable)
        .filter(
            RestaurantTable.restaurant_id == table.restaurant_id,
            RestaurantTable.table_number == table.table_number,
        )
        .first()
    )

    if existing_table:
        raise HTTPException(
            status_code=409,
            detail="This table number already exists for this restaurant",
        )

    db_table = RestaurantTable(**table.model_dump())

    db.add(db_table)
    db.commit()
    db.refresh(db_table)

    return db_table


@app.get("/tables", response_model=list[TableResponse])
def get_tables(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(RestaurantTable)
        .filter(RestaurantTable.restaurant_id == restaurant_id)
        .all()
    )


@app.get("/tables/{table_id}", response_model=TableResponse)
def get_table(
    table_id: int,
    db: Session = Depends(get_db),
):
    table = (
        db.query(RestaurantTable)
        .filter(RestaurantTable.id == table_id)
        .first()
    )

    if table is None:
        raise HTTPException(
            status_code=404,
            detail="Table not found",
        )

    return table



# --------------------------------
# MENU APIs - POSTGRESQL
# --------------------------------

@app.post("/menu", response_model=MenuItemResponse)
def create_menu_item(
    menu_item: MenuItemCreate,
    db: Session = Depends(get_db),
):
    # Check whether the restaurant exists
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == menu_item.restaurant_id)
        .first()
    )

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    db_menu_item = MenuItem(**menu_item.model_dump())

    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)

    return db_menu_item


@app.get("/menu", response_model=list[MenuItemResponse])
def get_menu(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(MenuItem)
        .filter(MenuItem.restaurant_id == restaurant_id)
        .all()
    )


@app.get("/menu/search", response_model=list[MenuItemResponse])
def search_menu(
    restaurant_id: int,
    q: str,
    db: Session = Depends(get_db),
):
    search_query = f"%{q}%"

    return (
        db.query(MenuItem)
        .filter(
            MenuItem.restaurant_id == restaurant_id,
            (MenuItem.name.ilike(search_query))
            | (MenuItem.description.ilike(search_query)),
        )
        .all()
    )


@app.get("/menu/{item_id}", response_model=MenuItemResponse)
def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    menu_item = (
        db.query(MenuItem)
        .filter(MenuItem.id == item_id)
        .first()
    )

    if menu_item is None:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found",
        )

    return menu_item



# --------------------------------
# HOME AND HEALTH
# --------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to DineVoice AI!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "DineVoice AI",
    }


# --------------------------------
# RESTAURANT APIs - POSTGRESQL
# --------------------------------

@app.post(
    "/restaurants",
    response_model=RestaurantResponse
)
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db),
):
    db_restaurant = Restaurant(**restaurant.model_dump())

    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


@app.get(
    "/restaurants",
    response_model=list[RestaurantResponse]
)
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()


@app.get(
    "/restaurants/{restaurant_id}",
    response_model=RestaurantResponse
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    return restaurant


# --------------------------------
# TABLE APIs - TEMPORARY STORAGE
# --------------------------------

@app.post("/tables", response_model=TableResponse)
def create_table(table: TableCreate):
    global next_table_id

    new_table = {
        "id": next_table_id,
        **table.model_dump(),
        "is_available": True,
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
        detail="Table not found",
    )


# --------------------------------
# MENU APIs - TEMPORARY STORAGE
# --------------------------------

@app.post("/menu", response_model=MenuItemResponse)
def create_menu_item(menu_item: MenuItemCreate):
    global next_menu_id

    new_menu_item = {
        "id": next_menu_id,
        **menu_item.model_dump(),
        "is_available": True,
    }

    menu_items.append(new_menu_item)
    next_menu_id += 1

    return new_menu_item


@app.get("/menu", response_model=list[MenuItemResponse])
def get_menu():
    return menu_items


# Keep search before /menu/{item_id}
@app.get(
    "/menu/search",
    response_model=list[MenuItemResponse]
)
def search_menu(q: str):
    search_query = q.lower()

    results = [
        item
        for item in menu_items
        if search_query in item["name"].lower()
        or search_query in item["description"].lower()
    ]

    return results


@app.get(
    "/menu/{item_id}",
    response_model=MenuItemResponse
)
def get_menu_item(item_id: int):
    for item in menu_items:
        if item["id"] == item_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Menu item not found",
    )
