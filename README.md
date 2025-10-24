# Food Delivery App

A Flask-based food delivery web application with MySQL database integration.

## Features

- Browse restaurants and their menus
- Add items to cart
- Place orders with delivery information
- Store data in MySQL database
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
     CREATE DATABASE food_delivery;
     ```

4. Configure database credentials:
   - Edit the `.env` file to match your MySQL configuration:
     ```
     MYSQL_HOST=localhost
     MYSQL_USER=your_mysql_username
     MYSQL_PASSWORD=your_mysql_password
     MYSQL_DB=food_delivery
     SECRET_KEY=your-secret-key-here
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

1. `restaurants` - Store restaurant information
2. `menu_items` - Store menu items for each restaurant
3. `orders` - Store order details
4. `order_items` - Store individual items in each order

## Project Structure

```
fooddelivery/
│
├── app.py              # Main Flask application
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed to version control)
├── .gitignore          # Git ignore file
├── README.md           # This file
│
├── templates/
│   ├── base.html               # Base template
│   ├── index.html              # Home page
│   ├── restaurant.html         # Restaurant menu page
│   ├── cart.html               # Shopping cart page
│   ├── checkout.html           # Checkout form
│   └── order_confirmation.html # Order confirmation page
```

## Technologies Used

- Flask (Python web framework)
- MySQL (Database)
- Bootstrap 5 (Frontend framework)
- Jinja2 (Template engine)
- python-dotenv (Environment variable management)

## Security Notes

- Database credentials are stored in `.env` file which is not committed to version control
- Never commit `.env` file to version control systems
- Generate a strong SECRET_KEY for production use

## Notes

- The application includes fallback mechanisms to use static data if the database connection fails
- Cart data is stored in memory (in a real application, you would use sessions or database storage)