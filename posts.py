from typing import Tuple, Any, Type

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import Users, Post, Topic, PostInteraction
from schemas import PostViewSchema
from utils import get_current_user, not_found, can_user_see_topic, access_denied

router = APIRouter(
    tags=["posts"]
)

def get_post_and_topic(post_id: int, user: Users, db: Session) -> tuple[Type[Post], Type[Topic]]:
    """
    Checks permission and existence of provided post and its topic/category
    """
    post = db.query(Post).filter(Post.id.__eq__(post_id)).first()
    if not post:
        raise not_found
    topic = db.query(Topic).filter(Topic.id.__eq__(post.topic_id)).first()
    if not topic:
        raise not_found
    if not can_user_see_topic(user, topic, db):
        raise access_denied
    return post, topic

@router.get("/{post_id}", response_model=PostViewSchema)
def get_post_data(post_id: int,
                  db: Session = Depends(get_db),
                  user: Users = Depends(get_current_user)
) -> PostViewSchema:
    """
    View post and its interactions
    """
    post, topic = get_post_and_topic(post_id, user, db)

    interactions = db.query(PostInteraction).filter(PostInteraction.post_id.__eq__(post_id)).all()
    sum_interactions = 0
    for interaction in interactions:
        sum_interactions += -1 if not interaction.vote else 1

    user_interaction = None

    for interaction in interactions:
        if interaction.user_id == user.id:
            user_interaction = interaction.vote

    result = PostViewSchema\
    (
        post=post,
        interactions=sum_interactions,
        user_vote=user_interaction
    )

    return result

@router.post("/{post_id}/interaction", response_model=PostViewSchema)
def add_or_change_user_interaction(post_id: int,
                  vote: int = Form(...),
                  db: Session = Depends(get_db),
                  user: Users = Depends(get_current_user)
) -> PostViewSchema:
    """
    Update or add post interaction. 1 for upvote, 0 to remove interaction, -1 for downvote
    """

    post, topic = get_post_and_topic(post_id, user, db)

    interaction = db.query(PostInteraction).filter\
    (
        PostInteraction.post_id.__eq__(post_id),
        PostInteraction.user_id.__eq__(user.id)
    ).first()

    interaction_type = True if vote == 1 else False if vote == -1 else None

    if interaction_type is None:
        if interaction:
            db.delete(interaction)
            db.commit()
    else:
        if interaction:
            interaction.vote = interaction_type
        else:
            interaction = PostInteraction\
            (
                vote=interaction_type,
                post_id=post_id,
                user_id=user.id
            )
            db.add(interaction)
        db.commit()

    interactions = db.query(PostInteraction).filter(PostInteraction.post_id.__eq__(post_id)).all()
    sum_votes = 0
    for interaction in interactions:
        sum_votes += -1 if not interaction.vote else 1

    return PostViewSchema\
    (
        post=post,
        interactions=sum_votes,
        user_vote=interaction_type
    )