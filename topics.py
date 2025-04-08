from typing import List

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from db import get_db
from models import Users, Topic, Post
from schemas import PostSchema
from utils import get_current_user, can_user_see_topic, not_found, access_denied

router = APIRouter(
    tags=["topics"]
)

@router.get("/{topic_id}", response_model=List[PostSchema])
def get_posts_in_topic(topic_id: int,
                       db: Session = Depends(get_db),
                       user: Users = Depends(get_current_user)
) -> list:
    """
    Lists all visible posts for the logged-in user
    """
    topic = db.query(Topic).filter(Topic.id.__eq__(topic_id)).first()

    if not topic:
        raise not_found

    if can_user_see_topic(user, topic, db):
        posts = db.query(Post).filter(Post.topic_id.__eq__(topic_id)).all()
        posts = [post for post in posts]
        return posts
    return []

@router.post("/{topic_id}/post", response_model=PostSchema)
def add_post(topic_id: int,
             db: Session = Depends(get_db),
             user: Users = Depends(get_current_user),
             content: str = Form(...)
) -> PostSchema:
    """
    Adds a post to topic
    """

    topic = db.query(Topic).filter(Topic.id.__eq__(topic_id)).first()

    if not topic:
        raise not_found

    if not can_user_see_topic(user, topic, db):
        raise access_denied

    post = Post\
    (
        content = content,
        user_id = user.id,
        topic_id = topic.id,
        category_id = topic.category_id
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    entry = db.query(Post).filter(Post.user_id.__eq__(user.id)).all()[-1]

    return PostSchema(id=entry.id,
                      content=content,
                      user_id=user.id,
                      topic_id=topic.id,
                      category_id=topic.category_id)