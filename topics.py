from typing import List, Type

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import Users, Category, Topic
from schemas import CategorySchema, TopicSchema
from utils import get_current_user, can_user_see_category, get_admin

router = APIRouter(
    tags=["category"]
)

@router.get("/", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db), user: Users = Depends(get_current_user)) -> list:
    """
    Lists all visible categories for the logged-in user
    :param db: database connection
    :param user: user requesting access
    :return: list of visible categories for logged-in user
    """
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
    """
    Adds a category to the database if the user is admin
    :param db: database connection
    :param admin: checks if user is an admin to verify permission
    :param name: name of category
    :param desc: description of category
    :return: a category entry in the database, including ID
    """

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

@router.get("/{category_id}", response_model=List[TopicSchema])
def get_topics_in_category\
        (category_id: int, db: Session = Depends(get_db), user: Users = Depends(get_current_user)) -> list[Type[Topic]]:
    """
    API request for all topics in a given category
    :param category_id: the id of the category
    :param db: database connection
    :param user: the user requesting access
    :return: list[topics in category]
    """

    category = db.query(Category).filter(Category.id.__eq__(category_id)).first()

    if (not category or
        not can_user_see_category(user, category, db)):
        raise HTTPException(status_code=403, detail="Invalid category")

    # Get all topics within this category
    topics = db.query(Topic).filter(Topic.category_id.__eq__(category.id)).all()
    return topics