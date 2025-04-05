-- Table: users
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(45) NOT NULL UNIQUE,
  password VARCHAR(45) NOT NULL,
  email VARCHAR(45) NOT NULL UNIQUE,
  age INT NOT NULL,
  nickname VARCHAR(45),
  registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
  admin BOOLEAN DEFAULT FALSE
);

-- Table: categories
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  description VARCHAR(255) NOT NULL,
  visibility BOOLEAN DEFAULT TRUE,
  locked BOOLEAN DEFAULT FALSE
);

-- Table: topics
DROP TABLE IF EXISTS topics;

CREATE TABLE topics (
  id VARCHAR(45) PRIMARY KEY,
  title VARCHAR(45) NOT NULL,
  description VARCHAR(255),
  locked BOOLEAN DEFAULT FALSE,
  user_id INT NOT NULL,
  category_id INT NOT NULL,
  CONSTRAINT fk_topics_users FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT fk_topics_categories FOREIGN KEY (category_id) REFERENCES categories (id)
);

-- Table: posts
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(45) NOT NULL,
  content TEXT NOT NULL,
  user_id INT NOT NULL,
  topic_id VARCHAR(45) NOT NULL,
  category_id INT NOT NULL,
  CONSTRAINT fk_posts_users FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT fk_posts_topics FOREIGN KEY (topic_id) REFERENCES topics (id),
  CONSTRAINT fk_posts_categories FOREIGN KEY (category_id) REFERENCES categories (id)
);

-- Table: replies
DROP TABLE IF EXISTS replies;

CREATE TABLE replies (
  id SERIAL PRIMARY KEY,
  post_id INT NOT NULL,
  reply_id INT,
  CONSTRAINT fk_replies_posts FOREIGN KEY (post_id) REFERENCES posts (id),
  CONSTRAINT fk_replies_replies FOREIGN KEY (reply_id) REFERENCES replies (id)
);

-- Table: topic_interactions
DROP TABLE IF EXISTS topic_interactions;

CREATE TABLE topic_interactions (
  id SERIAL PRIMARY KEY,
  vote BOOLEAN NOT NULL DEFAULT TRUE,
  topic_id VARCHAR(45) NOT NULL,
  user_id INT NOT NULL,
  CONSTRAINT fk_topic_interactions_topics FOREIGN KEY (topic_id) REFERENCES topics (id),
  CONSTRAINT fk_topic_interactions_users FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Table: post_interactions
DROP TABLE IF EXISTS post_interactions;

CREATE TABLE post_interactions (
  id SERIAL PRIMARY KEY,
  vote BOOLEAN NOT NULL DEFAULT TRUE,
  post_id INT NOT NULL,
  user_id INT NOT NULL,
  CONSTRAINT fk_post_interactions_posts FOREIGN KEY (post_id) REFERENCES posts (id),
  CONSTRAINT fk_post_interactions_users FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Table: replies_interactions
DROP TABLE IF EXISTS replies_interactions;

CREATE TABLE replies_interactions (
  id SERIAL PRIMARY KEY,
  vote BOOLEAN NOT NULL DEFAULT TRUE,
  reply_id INT NOT NULL,
  user_id INT NOT NULL,
  CONSTRAINT fk_replies_interactions_replies FOREIGN KEY (reply_id) REFERENCES replies (id),
  CONSTRAINT fk_replies_interactions_users FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Table: conversations
DROP TABLE IF EXISTS conversations;

CREATE TABLE conversations (
  id SERIAL PRIMARY KEY,
  date TIMESTAMP NOT NULL,
  initiator_id INT NOT NULL,
  receiver_id INT NOT NULL,
  CONSTRAINT fk_conversations_initiator FOREIGN KEY (initiator_id) REFERENCES users (id),
  CONSTRAINT fk_conversations_receiver FOREIGN KEY (receiver_id) REFERENCES users (id)
);

-- Table: direct_messages
DROP TABLE IF EXISTS direct_messages;

CREATE TABLE direct_messages (
  id SERIAL PRIMARY KEY,
  text VARCHAR(255) NOT NULL,
  date TIMESTAMP NOT NULL,
  conversation_id INT NOT NULL,
  sender_id INT NOT NULL,
  CONSTRAINT fk_direct_messages_conversations FOREIGN KEY (conversation_id) REFERENCES conversations (id),
  CONSTRAINT fk_direct_messages_sender FOREIGN KEY (sender_id) REFERENCES users (id)
);

-- Table: category_access_privileges
DROP TABLE IF EXISTS category_access_privileges;

CREATE TABLE category_access_privileges (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  category_id INT NOT NULL,
  permission_type BOOLEAN DEFAULT FALSE,
  CONSTRAINT fk_category_access_users FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT fk_category_access_categories FOREIGN KEY (category_id) REFERENCES categories (id)
);