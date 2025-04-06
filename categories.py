from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import Users, Category
from schemas import CategorySchema
from utils import get_current_user, can_user_see_category, get_admin

router = APIRouter(
    tags=["category"]
)

@router.get("/", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    categories = db.query(Category).all()
    visible_categories =\
    [
        category for category in categories
        if can_user_see_category(user, category, db)
    ]

    return visible_categories

@router.post("/add", response_model=CategorySchema)
def add_category\
    (db: Session = Depends(get_db), admin: Users = Depends(get_admin), name: str = Form(...), desc: str = Form(...)) -> CategorySchema:

    # Unique names check
    name_check = db.query(Category).filter(Category.name.__eq__(name)).first()
    if name_check:
        raise HTTPException(status_code=400, detail=f"Category with name {name} already exists.")

    new_category = Category\
    (
        name=name,
        description=desc,
        visibility=1,
        locked=False
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    entry = db.query(Category).filter(Category.name.__eq__(name)).first()

    return CategorySchema(id=entry.id, name=name, desc=desc)