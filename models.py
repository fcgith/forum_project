from sqlalchemy import Column, Integer, String, Boolean, Date, Text, ForeignKey, DateTime, CheckConstraint, \
    UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)  # Changed from 45 to 50
    hashed_password = Column(String(255), nullable=False)  # Changed from 45 to 255
    email = Column(String(100), unique=True, nullable=False)  # Changed from 45 to 100
    age = Column(Integer, CheckConstraint('age >= 0'))  # Added CHECK constraint
    nickname = Column(String(50))  # Changed from 45 to 50
    registration_date = Column(Date, nullable=False)  # Removed default=date.today
    admin = Column(Boolean, nullable=False, default=False)  # Added nullable=False

    topics = relationship("Topic", back_populates="user")
    posts = relationship("Post", back_populates="user")
    sent_messages = relationship("DirectMessage", foreign_keys="[DirectMessage.sender_id]", back_populates="sender")
    received_messages = relationship("Conversation", foreign_keys="[Conversation.receiver_id]",
                                     back_populates="receiver")
    post_interactions = relationship("PostInteraction", back_populates="user")
    category_privileges = relationship("CategoryAccessPrivilege", back_populates="user")
    # Removed replies, topic_interactions, reply_interactions as they're not in SQL


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)  # Changed from String(255), removed name
    visibility = Column(Boolean, nullable=False, default=True)  # Added nullable=False
    locked = Column(Boolean, nullable=False, default=False)  # Added nullable=False

    topics = relationship("Topic", back_populates="category")
    privileges = relationship("CategoryAccessPrivilege", back_populates="category")
    posts = relationship("Post", back_populates="category")
    # Removed name field as it's not in SQL


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)  # Changed from 45 to 100
    description = Column(Text)  # Changed from String(255)
    locked = Column(Boolean, nullable=False, default=False)  # Added nullable=False
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    user = relationship("Users", back_populates="topics")
    category = relationship("Category", back_populates="topics")
    posts = relationship("Post", back_populates="topic")
    # Removed interactions as it's not in SQL


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)  # Removed title
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    user = relationship("Users", back_populates="posts")
    topic = relationship("Topic", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    interactions = relationship("PostInteraction", back_populates="post")
    # Removed title and replies as they're not in SQL


class PostInteraction(Base):
    __tablename__ = "post_interactions"

    id = Column(Integer, primary_key=True)
    vote = Column(Boolean, nullable=False)  # Removed default=True
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint('post_id', 'user_id'),)  # Added unique constraint

    post = relationship("Post", back_populates="interactions")
    user = relationship("Users", back_populates="post_interactions")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)  # Changed from DateTime
    initiator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    initiator = relationship("Users", foreign_keys=[initiator_id], backref="initiated_conversations")
    receiver = relationship("Users", foreign_keys=[receiver_id], back_populates="received_messages")
    messages = relationship("DirectMessage", back_populates="conversation")


class DirectMessage(Base):
    __tablename__ = "direct_messages"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)  # Changed from String(255)
    date = Column(Date, nullable=False)  # Changed from DateTime
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("Users", back_populates="sent_messages")


class CategoryAccessPrivilege(Base):
    __tablename__ = "category_access_privileges"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    permission_type = Column(String(50), nullable=False)  # Changed from Boolean to String(50)

    __table_args__ = (UniqueConstraint('user_id', 'category_id'),)  # Added unique constraint

    user = relationship("Users", back_populates="category_privileges")
    category = relationship("Category", back_populates="privileges")