-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    age INTEGER CHECK (age >= 0),
    nickname VARCHAR(50),
    registration_date DATE NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create the categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    visibility BOOLEAN NOT NULL DEFAULT TRUE,
    locked BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create the topics table
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    locked BOOLEAN NOT NULL DEFAULT FALSE,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Create the posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Create the post_interactions table
CREATE TABLE post_interactions (
    id SERIAL PRIMARY KEY,
    vote BOOLEAN NOT NULL,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (post_id, user_id) -- Ensure a user can only vote once per post
);

-- Create the category_access_privileges table
CREATE TABLE category_access_privileges (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    permission_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE (user_id, category_id) -- Ensure unique access privileges per user and category
);

-- Create the conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    initiator_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    FOREIGN KEY (initiator_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create the direct_messages table
CREATE TABLE direct_messages (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    date DATE NOT NULL,
    conversation_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
);

-- categories table
CREATE INDEX idx_categories_visibility ON categories(visibility);
CREATE INDEX idx_categories_locked ON categories(locked);
CREATE INDEX idx_categories_visibility_locked ON categories(visibility, locked);

-- topics table
CREATE INDEX idx_topics_user_id ON topics(user_id);
CREATE INDEX idx_topics_category_id ON topics(category_id);
CREATE INDEX idx_topics_locked ON topics(locked);

-- posts table
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_topic_id ON posts(topic_id);
CREATE INDEX idx_posts_category_id ON posts(category_id);

-- post_interactions table
CREATE INDEX idx_post_interactions_user_id ON post_interactions(user_id);

-- category_access_privileges table
CREATE INDEX idx_category_access_privileges_category_id ON category_access_privileges(category_id);

-- conversations table
CREATE INDEX idx_conversations_initiator_id ON conversations(initiator_id);
CREATE INDEX idx_conversations_receiver_id ON conversations(receiver_id);
CREATE INDEX idx_conversations_date ON conversations(date);

-- direct_messages table
CREATE INDEX idx_direct_messages_conversation_id ON direct_messages(conversation_id);
CREATE INDEX idx_direct_messages_sender_id ON direct_messages(sender_id);
CREATE INDEX idx_direct_messages_date ON direct_messages(date);
CREATE INDEX idx_direct_messages_conversation_id_date ON direct_messages(conversation_id, date);