# Foodle - Food Delivery App

A Flask-based food delivery web application with MySQL database integration.

## Features

- Browse restaurants and menus
- Add items to cart with quantity controls
- Place orders with customer information
- View order history
- Manage customers and drivers
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
   
   This will create all necessary tables and populate them with sample data 

## Running the Application

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`

## Database Schema

The application automatically creates the following tables:

1. `customers` - Store customer information (customer_id, name, email, address)
2. `restaurants` - Store restaurant information (restaurant_id, name, address, phone_number)
3. `drivers` - Store delivery driver information (driver_id, name, phone_number)
4. `menu_items` - Store menu items for each restaurant (menu_item_id, restaurant_id, name, description, price) - directly linked to restaurants without a separate menus table
5. `orders` - Store order details (order_id, customer_id, restaurant_id, driver_id, order_date)
6. `order_items` - Store individual items in each order (order_item_id, order_id, menu_item_id, quantity)

## Project Structure

- `app.py` - Main Flask application
- `init_db.py` - Database initialization script that executes schema.sql
- `schema.sql` - Complete database schema in pure SQL
- `templates/` - HTML templates using Jinja2
- `.env` - Environment configuration file
- `requirements.txt` - Python dependencies