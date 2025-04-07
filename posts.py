from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from models import Users, Post, Topic, PostInteraction
from schemas import PostViewSchema
from utils import get_current_user, not_found, can_user_see_topic, access_denied

router = APIRouter(
    tags=["posts"]
)

@router.get("/{post_id}", response_model=PostViewSchema)
def get_post_data(post_id: int,
                       db: Session = Depends(get_db),
                       user: Users = Depends(get_current_user)) -> PostViewSchema:
    """
    View post and its interactions
    """

    post = db.query(Post).filter(Post.id.__eq__(post_id)).first()

    if not post:
        raise not_found

    topic = db.query(Topic).filter(Topic.id.__eq__(post.topic_id)).first()

    if not topic:
        raise not_found

    if can_user_see_topic(user, topic, db):
        interactions = db.query(PostInteraction).filter(PostInteraction.post_id.__eq__(post_id)).all()
        votes = sum([interaction.vote for interaction in interactions]) if interactions else 0

        user_interaction = None

        for interaction in interactions:
            if interaction.user_id == user.id:
                user_interaction = interaction.vote

        result = PostViewSchema\
        (
            post=post,
            interactions=votes,
            user_vote=user_interaction
        )

        return result
    raise access_denied