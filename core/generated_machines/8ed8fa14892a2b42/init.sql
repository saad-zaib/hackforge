CREATE DATABASE IF NOT EXISTS hackforge;
USE hackforge;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(255),
    email VARCHAR(100),
    role VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS secrets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    flag VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP
);

INSERT INTO users (username, password, email, role) VALUES ('admin', 'admin123', 'admin@hack.com', 'admin');
INSERT INTO users (username, password, email, role) VALUES ('user', 'password', 'user@hack.com', 'user');
INSERT INTO secrets (flag, description, created_at) VALUES ('HACKFORGE{a37513f5dd834fba337541d69ec150ba}', 'Capture this flag!', NOW());

