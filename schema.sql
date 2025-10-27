SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS customers;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

CREATE TABLE drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

CREATE TABLE menus (
    menu_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

CREATE TABLE menu_items (
    menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    driver_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id)
);

INSERT INTO restaurants (name, address, phone_number) VALUES
('Dominos', 'SJT, VIT-Vellore, Tamil Nadu 632014', '+91-999999999'),
('McDonalds', 'Katpadi Main Road, Vellore, Tamil Nadu 632014', '+91-999999998'),
('Tara Ma', 'Near VIT Main Gate, Vellore, Tamil Nadu 632014', '+91-999999997'),
('Shareef Briyani', 'Katpadi Main Road, Vellore, Tamil Nadu 632014', '+91-999999996'),
('Aunty Mess', 'Near VIT Main Gate, Vellore, Tamil Nadu 632014', '+91-999999995'),
('Vellore Kitchen', 'Gandhi Road, Vellore, Tamil Nadu 632002', '+91-999999994');

INSERT INTO drivers (name, phone_number) VALUES
('Rahul Mishra', '+91-999999999'),
('Suraj Kumar', '+91-999999998'),
('Vivek Verma', '+91-999999997'),
('Arjun Patel', '+91-999999996'),
('Karan Singh', '+91-999999995');

INSERT INTO menu_items (restaurant_id, name, description, price) VALUES
(1, 'Margherita Pizza', 'Classic pizza with pizza sauce and mozzarella', 199.99),
(1, 'Pepperoni Pizza', 'Pizza topped with spicy pepperoni slices', 249.99),
(1, 'Veggie Supreme Pizza', 'Pizza loaded with mushrooms, onions, olives and capsicum', 299.99),
(1, 'Garlic Breadsticks', 'Freshly baked breadsticks with garlic seasoning', 99.99),
(2, 'Veggie Burger', 'Burger with lettuce, tomato, and cheese', 99.99),
(2, 'Cheese Fries', 'Crispy fries topped with melted cheese', 105.99),
(2, 'McAloo Tikki Burger', 'Indian style veg burger with spicy aloo patty', 79.99),
(2, 'McFlurry', 'Vanilla ice cream with chocolate chunks', 49.99),
(3, 'Paneer Butter Masala', 'Spicy cottage cheese gravy', 159.99),
(3, 'Chicken Tikka Masala', 'Spicy chicken gravy', 179.99),
(3, 'Dal Makhani', 'Creamy black lentils cooked overnight', 139.99),
(3, 'Naan', 'Freshly baked Indian bread', 49.99),
(4, 'Chicken Dum Biryani', 'Traditional Hyderabadi biryani with tender chicken', 199.99),
(4, 'Mutton Biryani', 'Flavorful biryani with succulent mutton pieces', 249.99),
(4, 'Raita', 'Curd with cucumber and mint', 69.99),
(4, 'Chicken 65', 'Spicy fried chicken starter', 179.99),
(5, 'Masala Dosa', 'Crispy dosa with potato filling and chutneys', 129.99),
(5, 'Idli Sambhar', 'Soft steamed idlis with hot sambhar', 99.99),
(5, 'Vada', 'Crispy fried lentil fritters with coconut chutney', 89.99),
(5, 'Pongal', 'Rice and lentil dish with ghee and cashews', 109.99),
(6, 'Filter Coffee', 'Traditional South Indian coffee', 49.99),
(6, 'Ghee Roast Dosa', 'Crispy dosa with ghee and potato filling', 149.99),
(6, 'Upma', 'Semolina cooked with vegetables and spices', 79.99),
(6, 'Puri Bhaji', 'Deep fried bread with spicy potato curry', 99.99);





