from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import Users, Topic, Post
from schemas import PostSchema
from utils import get_current_user, can_user_see_topic

router = APIRouter(
    tags=["topics"]
)

@router.get("/{topic_id}", response_model=List[PostSchema])
def get_posts_in_topic(topic_id: int, db: Session = Depends(get_db), user: Users = Depends(get_current_user)) -> list:
    """
    Lists all visible posts for the logged-in user
    :param topic_id: the category
    :param db: database connection
    :param user: user requesting access
    :return: list of visible categories for logged-in user
    """
    topic = db.query(Topic).filter(Topic.id.__eq__(topic_id)).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    if can_user_see_topic(user, topic, db):
        posts = db.query(Post).filter(Post.topic_id.__eq__(topic_id)).all()
        posts =\
        [
            post for post in posts
        ]
        return posts
    return []