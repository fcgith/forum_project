from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from db import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(45), unique=True, index=True, nullable=False)
    hashed_password = Column(String(64), nullable=False)
    email = Column(String(45), nullable=False)
    age = Column(Integer, nullable=False)
    nickname = Column(String(45), nullable=True)
    admin = Column(Integer, nullable=True)

    # Relationships
    topics = relationship("Topic", back_populates="user")
    posts = relationship("Post", back_populates="user")
    replies = relationship("Reply", back_populates="user")
    sent_messages = relationship("DirectMessage", foreign_keys="DirectMessage.initiator_id", back_populates="initiator")
    received_messages = relationship("DirectMessage", foreign_keys="DirectMessage.receiver_id", back_populates="receiver")
    topic_interactions = relationship("TopicInteraction", back_populates="user")
    post_interactions = relationship("PostInteraction", back_populates="user")
    reply_interactions = relationship("ReplyInteraction", back_populates="user")
    category_privileges = relationship("CategoryAccessPrivilege", back_populates="user")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(45), nullable=False)
    description = Column(String(255), nullable=True)
    locked = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Relationships
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

    # Relationships
    user = relationship("Users", back_populates="posts")
    topic = relationship("Topic", back_populates="posts")
    replies = relationship("Reply", back_populates="post")
    interactions = relationship("PostInteraction", back_populates="post")

class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(45), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    # Relationships
    user = relationship("Users", back_populates="replies")
    post = relationship("Post", back_populates="replies")
    interactions = relationship("ReplyInteraction", back_populates="reply")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), nullable=False)
    description = Column(String(255), nullable=True)
    visibility = Column(Boolean, default=True)
    locked = Column(Boolean, default=False)

    # Relationships
    topics = relationship("Topic", back_populates="category")
    privileges = relationship("CategoryAccessPrivilege", back_populates="category")

class DirectMessage(Base):
    __tablename__ = "direct_messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    initiator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    initiator = relationship("Users", foreign_keys=[initiator_id], back_populates="sent_messages")
    receiver = relationship("Users", foreign_keys=[receiver_id], back_populates="received_messages")

class TopicInteraction(Base):
    __tablename__ = "topic_interaction"

    id = Column(Integer, primary_key=True, index=True)
    vote = Column(Boolean, nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    topic = relationship("Topic", back_populates="interactions")
    user = relationship("Users", back_populates="topic_interactions")

class PostInteraction(Base):
    __tablename__ = "post_interaction"

    id = Column(Integer, primary_key=True, index=True)
    vote = Column(Boolean, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    post = relationship("Post", back_populates="interactions")
    user = relationship("Users", back_populates="post_interactions")

class ReplyInteraction(Base):
    __tablename__ = "reply_interaction"

    id = Column(Integer, primary_key=True, index=True)
    vote = Column(Boolean, nullable=False)
    reply_id = Column(Integer, ForeignKey("replies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    reply = relationship("Reply", back_populates="interactions")
    user = relationship("Users", back_populates="reply_interactions")

class CategoryAccessPrivilege(Base):
    __tablename__ = "category_access_privileges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    permission_type = Column(Boolean, nullable=False)

    # Relationships
    user = relationship("Users", back_populates="category_privileges")
    category = relationship("Category", back_populates="privileges")