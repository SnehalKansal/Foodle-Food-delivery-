# Foodle - Food Delivery App

A Flask-based food delivery web application with MySQL database integration.

## Features

- Browse restaurants and their menus
- Add items to cart
- Place orders with customer information (name, email, address, phone)
- View order history and status
- Manage customers and delivery drivers
- Store all data in MySQL database
- Secure credential management with .env file

## Prerequisites

- Python 3.6+
- MySQL Server
- pip (Python package installer)

## Installation

1. Clone or download this repository

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up MySQL database:
   - Install MySQL Server if not already installed
   - Create a database for the application:
     ```sql
     CREATE DATABASE foodel;
     ```

4. Configure database credentials:
   - Edit the `.env` file to match your MySQL configuration:
     ```
     MYSQL_HOST=localhost
     MYSQL_USER=your_mysql_username
     MYSQL_PASSWORD=your_mysql_password
     MYSQL_DB=foodel
     ```

5. Initialize the database with sample data:
   ```
   python init_db.py
   ```

## Running the Application

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`

## Database Schema

The application automatically creates the following tables:

1. `customers` - Store customer information (name, email, address)
2. `restaurants` - Store restaurant information (name, address, phone)
3. `drivers` - Store delivery driver information (name, phone)
4. `menus` - Store restaurant menus
5. `menu_items` - Store menu items for each restaurant with prices in Rs.
6. `orders` - Store order details (customer, restaurant, driver, status)
7. `order_items` - Store individual items in each order



