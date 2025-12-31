# app/routes/item.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.get_db import get_db
from app.models import Item as ItemModel
from app.schemas._global import ApiResponse
from app.schemas.item import Item as ItemSchema

router = APIRouter()

@router.post("/", response_model=ApiResponse[ItemSchema])
def create_item(item_name: str, db: Session = Depends(get_db)):
    db_item = ItemModel(name=item_name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    item_out = ItemSchema.model_validate(db_item)
    return ApiResponse(
        status_code=201,
        message="생성됨",
        result=item_out
    )

@router.get("/{item_id}", response_model=ApiResponse[ItemSchema])
def read_item(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} not found."
        )
    return ApiResponse(
        status_code=200,
        message="성공",
        result=ItemSchema.model_validate(db_item)
    )
