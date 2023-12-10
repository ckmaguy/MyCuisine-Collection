-- Create the 'test_mycuisine_db' database for testing
CREATE DATABASE test_mycuisine_db;

-- Select the 'test_mycuisine_db' database for use
USE test_mycuisine_db;

-- Create the 'users' table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(512) NOT NULL
);

-- Add additional columns to 'users' table
ALTER TABLE users
ADD COLUMN date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN profile_picture VARCHAR(256);

-- Create the 'recipe' table
CREATE TABLE recipe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    user_id INT,
    ingredients TEXT,
    preparation_time INT,
    cooking_time INT,
    servings INT,
    steps TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Optionally, create or grant access to a user specifically for testing
-- CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpassword';
-- GRANT ALL PRIVILEGES ON test_mycuisine_db.* TO 'testuser'@'localhost';

-- Flush the privileges to ensure changes take effect
FLUSH PRIVILEGES;
