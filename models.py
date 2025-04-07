from datetime import date

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from db import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(45), unique=True, index=True, nullable=False)
    hashed_password = Column(String(45), nullable=False)
    email = Column(String(45), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    nickname = Column(String(45))
    registration_date = Column(Date, nullable=False, default=date.today)
    admin = Column(Boolean, default=False)

    topics = relationship("Topic", back_populates="user")
    posts = relationship("Post", back_populates="user")
    replies = relationship("Reply", back_populates="user")
    sent_messages = relationship("DirectMessage", foreign_keys="[DirectMessage.sender_id]", back_populates="sender")
    received_messages = relationship("Conversation", foreign_keys="[Conversation.receiver_id]", back_populates="receiver")
    topic_interactions = relationship("TopicInteraction", back_populates="user")
    post_interactions = relationship("PostInteraction", back_populates="user")
    reply_interactions = relationship("ReplyInteraction", back_populates="user")
    category_privileges = relationship("CategoryAccessPrivilege", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False)
    description = Column(String(255), nullable=False)
    visibility = Column(Boolean, default=True)
    locked = Column(Boolean, default=False)

    topics = relationship("Topic", back_populates="category")
    privileges = relationship("CategoryAccessPrivilege", back_populates="category")
    posts = relationship("Post", back_populates="category")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(45), nullable=False)
    description = Column(String(255))
    locked = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    user = relationship("Users", back_populates="topics")
    category = relationship("Category", back_populates="topics")
    posts = relationship("Post", back_populates="topic")
    interactions = relationship("TopicInteraction", back_populates="topic")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(45), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    user = relationship("Users", back_populates="posts")
    topic = relationship("Topic", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    replies = relationship("Reply", back_populates="post")
    interactions = relationship("PostInteraction", back_populates="post")

class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    reply_id = Column(Integer, ForeignKey("replies.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # <-- Add this

    post = relationship("Post", back_populates="replies")
    parent_reply = relationship("Reply", remote_side=[id])
    interactions = relationship("ReplyInteraction", back_populates="reply")
    user = relationship("Users", back_populates="replies")  # <-- Add this


class TopicInteraction(Base):
    __tablename__ = "topic_interactions"

    id = Column(Integer, primary_key=True, index=True)
    vote = Column(Boolean, nullable=False, default=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    topic = relationship("Topic", back_populates="interactions")
    user = relationship("Users", back_populates="topic_interactions")

class PostInteraction(Base):
    __tablename__ = "post_interactions"

    id = Column(Integer, primary_key=True, index=True)
    vote = Column(Boolean, nullable=False, default=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    post = relationship("Post", back_populates="interactions")
    user = relationship("Users", back_populates="post_interactions")

class ReplyInteraction(Base):
    __tablename__ = "replies_interactions"

    id = Column(Integer, primary_key=True, index=True)
    vote = Column(Boolean, nullable=False, default=True)
    reply_id = Column(Integer, ForeignKey("replies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    reply = relationship("Reply", back_populates="interactions")
    user = relationship("Users", back_populates="reply_interactions")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    initiator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    initiator = relationship("Users", foreign_keys=[initiator_id], backref="initiated_conversations")
    receiver = relationship("Users", foreign_keys=[receiver_id], back_populates="received_messages")
    messages = relationship("DirectMessage", back_populates="conversation")

class DirectMessage(Base):
    __tablename__ = "direct_messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("Users", back_populates="sent_messages")

class CategoryAccessPrivilege(Base):
    __tablename__ = "category_access_privileges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    permission_type = Column(Boolean, default=False, nullable=True)

    user = relationship("Users", back_populates="category_privileges")
    category = relationship("Category", back_populates="privileges")
