CREATE DATABASE IF NOT EXISTS hackforge;
USE hackforge;

CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    author VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(255),
    session_token VARCHAR(255),
    secret_data TEXT
);

INSERT INTO comments (username, comment, created_at) VALUES ('admin', 'Welcome to our platform!', NOW());
INSERT INTO comments (username, comment, created_at) VALUES ('user1', 'Great website!', NOW());
INSERT INTO posts (title, content, author, created_at) VALUES ('Welcome Post', 'This is the first post on our platform.', 'admin', NOW());
INSERT INTO users (username, email, session_token, secret_data) VALUES ('admin', 'admin@hackforge.local', 'admin_secret_token_12345', 'HACKFORGE{2a7334922c22a51f69fdb00801c690bf}');
INSERT INTO users (username, email, session_token, secret_data) VALUES ('user1', 'user1@hackforge.local', 'user_token_67890', 'Regular user data');

