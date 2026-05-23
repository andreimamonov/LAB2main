from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas
from typing import Optional, Tuple

class ItemService:
    """Сервис для работы с Item (мягкое удаление, пагинация)"""

    @staticmethod
    def create(db: Session, item_data: schemas.ItemCreate) -> models.Item:
        """Создать новый элемент"""
        db_item = models.Item(
            name=item_data.name,
            description=item_data.description,
            status=item_data.status
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_active_by_id(db: Session, item_id: int) -> Optional[models.Item]:
        """Получить активный (не удалённый) элемент по ID"""
        return db.query(models.Item).filter(
            models.Item.id == item_id,
            models.Item.deleted_at.is_(None)
        ).first()

    @staticmethod
    def update(db: Session, db_item: models.Item, update_data: schemas.ItemUpdate) -> models.Item:
        """Частичное обновление элемента (PATCH)"""
        if update_data.name is not None:
            db_item.name = update_data.name
        if update_data.description is not None:
            db_item.description = update_data.description
        if update_data.status is not None:
            db_item.status = update_data.status
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def soft_delete(db: Session, db_item: models.Item) -> None:
        """Мягкое удаление (установить deleted_at)"""
        db_item.deleted_at = func.now()
        db.commit()

    @staticmethod
    def get_active_paginated(db: Session, page: int, limit: int) -> Tuple[list[models.Item], int]:
        """
        Вернуть список активных элементов с пагинацией и общее количество
        Возвращает: (список_элементов, общее_количество_активных)
        """
        query = db.query(models.Item).filter(models.Item.deleted_at.is_(None))
        total = query.count()
        items = query.order_by(models.Item.id.desc()) \
                     .offset((page - 1) * limit) \
                     .limit(limit) \
                     .all()
        return items, total