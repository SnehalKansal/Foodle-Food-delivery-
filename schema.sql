-- Disable foreign key checks temporarily
SET FOREIGN_KEY_CHECKS = 0;

-- Drop tables in correct order
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS customers;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Create customers table
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    address TEXT NOT NULL
);

-- Create restaurants table
CREATE TABLE restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

-- Create drivers table
CREATE TABLE drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

-- Create menu_items table (direct link to restaurant)
CREATE TABLE menu_items (
    menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- Create orders table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    driver_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
);

-- Create order_items table
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id)
);

-- Insert sample restaurants
INSERT INTO restaurants (name, address, phone_number) VALUES
('Dominos', 'SJT, VIT-Vellore', '+91-999999999'),
('McDonalds', 'Katpadi, Vellore', '+91-999999999'),
('Tara Ma', 'Katpadi, Vellore', '+91-999999999');

-- Insert sample drivers
INSERT INTO drivers (name, phone_number) VALUES
('Rahul Mishra', '+91-999999999'),
('Suraj Kumar', '+91-999999999'),
('Vivek Verma', '+91-999999999');

-- Insert sample menu items
INSERT INTO menu_items (restaurant_id, name, description, price) VALUES
(1, 'Margherita Pizza', 'Classic pizza with tomato sauce and mozzarella', 190.99),
(1, 'Pepperoni Pizza', 'Pizza topped with spicy pepperoni slices', 205.99),
(2, 'Classic Burger', 'Burger with lettuce, tomato, and cheese', 110.99),
(2, 'Cheese Fries', 'Crispy fries topped with melted cheese', 105.99),
(3, 'Paneer Butter Masala', 'Spicy cottage cheese gravy', 160.99),
(3, 'Chicken Tikka Masala', 'Spicy chicken gravy', 180.99);

