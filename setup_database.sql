-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS shoppin_item;
USE Items_list;

-- Step 2: Create the 'items' table
CREATE TABLE IF NOT EXISTS items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Step 3: Insert sample data
INSERT INTO items (item_name, price) VALUES 
('Apple', 1.50),
('Banana', 0.50),
('Orange', 1.00),
('Milk', 2.00),
('Bread', 2.50),
('Eggs', 3.00),
('Rice', 5.00),
('Sugar', 1.20),
('Salt', 0.80),
('Chicken', 7.50);
