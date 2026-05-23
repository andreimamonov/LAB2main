from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import services, schemas

router = APIRouter(prefix="/items", tags=["items"])

# ---- GET /items (список с пагинацией) ----
@router.get("/", response_model=schemas.PaginatedResponse)
def get_items(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    items, total = services.ItemService.get_active_paginated(db, page, limit)
    total_pages = (total + limit - 1) // limit

    return {
        "data": [schemas.ItemResponse.model_validate(item) for item in items],
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    }

# ---- GET /items/{id} (получить один элемент) ----
@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = services.ItemService.get_active_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# ---- POST /items (создать) ----
@router.post("/", response_model=schemas.ItemResponse, status_code=201)
def create_item(item_data: schemas.ItemCreate, db: Session = Depends(get_db)):
    return services.ItemService.create(db, item_data)

# ---- PUT /items/{id} (полное обновление) ----
@router.put("/{item_id}", response_model=schemas.ItemResponse)
def update_item_full(item_id: int, item_data: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = services.ItemService.get_active_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    # Обновляем все поля
    item.name = item_data.name
    item.description = item_data.description
    item.status = item_data.status
    db.commit()
    db.refresh(item)
    return item

# ---- PATCH /items/{id} (частичное обновление) ----
@router.patch("/{item_id}", response_model=schemas.ItemResponse)
def update_item_partial(item_id: int, item_data: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = services.ItemService.get_active_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = services.ItemService.update(db, item, item_data)
    return updated

# ---- DELETE /items/{id} (мягкое удаление) ----
@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = services.ItemService.get_active_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    services.ItemService.soft_delete(db, item)
    return None