from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Database configuration - loaded from .env file
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'food_delivery')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Function to create a database connection
def create_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

# Function to initialize the database with tables
def init_db():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        
        # Create customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                address TEXT NOT NULL
            )
        """)
        
        # Create restaurants table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurants (
                restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                address TEXT NOT NULL,
                phone_number VARCHAR(20) NOT NULL
            )
        """)
        
        # Create drivers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drivers (
                driver_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                vehicle_details TEXT
            )
        """)
        
        # Create menus table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menus (
                menu_id INT AUTO_INCREMENT PRIMARY KEY,
                restaurant_id INT NOT NULL,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
            )
        """)
        
        # Create menu_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
                menu_id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (menu_id) REFERENCES menus(menu_id)
            )
        """)
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                restaurant_id INT NOT NULL,
                driver_id INT,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'pending',
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
                FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
            )
        """)
        
        # Create order_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                menu_item_id INT NOT NULL,
                quantity INT DEFAULT 1,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id)
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()

# Initialize the database when the app starts
init_db()

# In-memory cart (in a real app, you might want to store this in the session or database)
cart = []

@app.route('/')
def index():
    # Fetch restaurants from database
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM restaurants")
    db_restaurants = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', restaurants=db_restaurants, cart_count=len(cart))

@app.route('/restaurant/<int:restaurant_id>')
def restaurant(restaurant_id):
    # Fetch restaurant and menu items from database
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Get restaurant details
    cursor.execute("SELECT * FROM restaurants WHERE restaurant_id = %s", (restaurant_id,))
    restaurant = cursor.fetchone()
    
    if not restaurant:
        cursor.close()
        connection.close()
        return "Restaurant not found", 404
    
    # Get menu items for this restaurant
    cursor.execute("""
        SELECT mi.* 
        FROM menu_items mi 
        JOIN menus m ON mi.menu_id = m.menu_id 
        WHERE m.restaurant_id = %s
    """, (restaurant_id,))
    items = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return render_template('restaurant.html', restaurant=restaurant, items=items, cart_count=len(cart))

@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    # Fetch item from database
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items WHERE menu_item_id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if item:
        cart.append(item)
        
    return redirect(url_for('cart_page'))

@app.route('/cart')
def cart_page():
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total, cart_count=len(cart))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Save order to database
        connection = create_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            
            # For now, we'll create a simple customer record
            # In a real app, you'd have proper customer management
            customer_name = request.form['name']
            customer_email = request.form['email']  # Use the provided email
            customer_address = request.form['address']
            
            # Insert customer (in a real app, you'd check if they already exist)
            cursor.execute("""
                INSERT INTO customers (name, email, address) 
                VALUES (%s, %s, %s)
            """, (customer_name, customer_email, customer_address))
            customer_id = cursor.lastrowid
            
            # For simplicity, assign order to restaurant 1 and driver 1
            # In a real app, you'd have logic to determine these
            restaurant_id = 1
            driver_id = 1
            
            # Insert order (removed total_amount since it's not in the schema)
            cursor.execute("""
                INSERT INTO orders (customer_id, restaurant_id, driver_id, status)
                VALUES (%s, %s, %s, %s)
            """, (customer_id, restaurant_id, driver_id, 'pending'))
            order_id = cursor.lastrowid
            
            # Insert order items
            for item in cart:
                cursor.execute("""
                    INSERT INTO order_items (order_id, menu_item_id, quantity)
                    VALUES (%s, %s, %s)
                """, (order_id, item['menu_item_id'], 1))
            
            connection.commit()
            
            # Prepare order details for confirmation page
            total_amount = sum(item['price'] for item in cart)
            order_details = {
                'order_id': order_id,
                'customer_name': customer_name,
                'customer_email': customer_email,  # Add email to order details
                'delivery_address': customer_address,
                'items': cart.copy(),
                'total': total_amount
            }
            
            # Clear the cart
            cart.clear()
            cursor.close()
            connection.close()
            return render_template('order_confirmation.html', order=order_details, cart_count=len(cart))
        except Error as e:
            print(f"Error saving order: {e}")
            connection.rollback()
            if cursor:
                cursor.close()
            connection.close()
            # Prepare order details for confirmation page even if there was an error
            order_details = {
                'customer_name': request.form['name'],
                'customer_email': request.form['email'],  # Add email to fallback
                'delivery_address': request.form['address'],
                'phone': request.form.get('phone', ''),
                'items': cart.copy(),
                'total': sum(item['price'] for item in cart)
            }
            cart.clear()
            return render_template('order_confirmation.html', order=order_details, cart_count=len(cart))
    
    total = sum(item['price'] for item in cart)
    return render_template('checkout.html', total=total, cart_count=len(cart))

@app.route('/customers')
def customers():
    # Fetch customers from database
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    db_customers = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('customers.html', customers=db_customers, cart_count=len(cart))

@app.route('/drivers')
def drivers():
    # Fetch drivers from database
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM drivers")
    db_drivers = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('drivers.html', drivers=db_drivers, cart_count=len(cart))

@app.route('/orders')
def orders():
    # Fetch orders from database
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.*, c.name as customer_name, c.email as customer_email, r.name as restaurant_name, d.name as driver_name,
               COALESCE(SUM(mi.price * oi.quantity), 0) as total_amount
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id
        LEFT JOIN drivers d ON o.driver_id = d.driver_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        LEFT JOIN menu_items mi ON oi.menu_item_id = mi.menu_item_id
        GROUP BY o.order_id, c.name, c.email, r.name, d.name
    """)
    db_orders = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('orders.html', orders=db_orders, cart_count=len(cart))

if __name__ == '__main__':
    app.run(debug=True)