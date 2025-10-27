from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'food_delivery')

def create_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

# Initialize cart as a list of dictionaries with quantity
cart = []

@app.route('/')
def index():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM restaurants")
    db_restaurants = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', restaurants=db_restaurants, cart_count=len(cart))

@app.route('/restaurant/<int:restaurant_id>')
def restaurant(restaurant_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Get restaurant details
    cursor.execute("SELECT * FROM restaurants WHERE restaurant_id = %s", (restaurant_id,))
    db_restaurant = cursor.fetchone()
    
    # Get menu items for this restaurant
    cursor.execute("""
        SELECT mi.*, r.name as restaurant_name 
        FROM menu_items mi 
        JOIN restaurants r ON mi.restaurant_id = r.restaurant_id 
        WHERE mi.restaurant_id = %s
    """, (restaurant_id,))
    db_items = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('restaurant.html', restaurant=db_restaurant, items=db_items, cart=cart, cart_count=len(cart))

@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT menu_item_id, restaurant_id, name, description, price FROM menu_items WHERE menu_item_id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if item:
        # Convert tuple to list to access by index
        item_list = list(item)
        
        # Create a dictionary from the list result
        item_dict = {
            'menu_item_id': item_list[0],
            'restaurant_id': item_list[1],
            'name': item_list[2],
            'description': item_list[3],
            'price': float(str(item_list[4])) if item_list[4] else 0.0
        }
        
        # Get restaurant name for the cart message
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM restaurants WHERE restaurant_id = %s", (item_dict['restaurant_id'],))
        restaurant = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if restaurant:
            restaurant_list = list(restaurant)
            item_dict['restaurant_name'] = restaurant_list[0]
        
        # Check if item already exists in cart
        existing_item = None
        for i, cart_item in enumerate(cart):
            if cart_item['menu_item_id'] == item_dict['menu_item_id']:
                existing_item = i
                break
        
        if existing_item is not None:
            # Increase quantity if item already in cart
            cart[existing_item]['quantity'] += 1
        else:
            # Add new item with quantity 1
            item_dict['quantity'] = 1
            cart.append(item_dict)
        
    return redirect(url_for('cart_page'))

@app.route('/update_quantity/<int:item_id>/<string:action>')
def update_quantity(item_id, action):
    # Find the item in cart
    for i, item in enumerate(cart):
        if item['menu_item_id'] == item_id:
            if action == 'increase':
                cart[i]['quantity'] += 1
            elif action == 'decrease' and item['quantity'] > 1:
                cart[i]['quantity'] -= 1
            elif action == 'decrease' and item['quantity'] == 1:
                # Remove item if quantity would be 0
                cart.pop(i)
            break
    
    return redirect(url_for('cart_page'))

@app.route('/cart')
def cart_page():
    total = sum(float(str(item['price'])) * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total, cart_count=len(cart))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        connection = create_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            
            customer_name = request.form['name']
            customer_email = request.form['email']
            customer_address = request.form['address']
            customer_phone = request.form['phone']  # Get phone number from form
            
            cursor.execute("""
                INSERT INTO customers (name, email, address) 
                VALUES (%s, %s, %s)
            """, (customer_name, customer_email, customer_address))
            customer_id = cursor.lastrowid
            
            # Use the restaurant_id from the first item in the cart
            restaurant_id = cart[0]['restaurant_id'] if cart else 1
            
            # Get the count of existing orders to determine which driver to assign
            cursor.execute("SELECT COUNT(*) FROM orders")
            order_count_result = cursor.fetchone()
            order_count_list = list(order_count_result) if order_count_result else [0]
            order_count = int(str(order_count_list[0])) if order_count_list else 0
            
            # Get all available drivers
            cursor.execute("SELECT driver_id FROM drivers")
            drivers = cursor.fetchall()
            
            # Assign driver using round-robin approach
            if drivers:
                driver_list = []
                for driver in drivers:
                    driver_item_list = list(driver)
                    driver_list.append(int(str(driver_item_list[0])))
                driver_id = driver_list[order_count % len(driver_list)]
            else:
                driver_id = None  # No drivers available
            
            cursor.execute("""
                INSERT INTO orders (customer_id, restaurant_id, driver_id)
                VALUES (%s, %s, %s)
            """, (customer_id, restaurant_id, driver_id))
            order_id = cursor.lastrowid
            
            for item in cart:
                cursor.execute("""
                    INSERT INTO order_items (order_id, menu_item_id, quantity)
                    VALUES (%s, %s, %s)
                """, (order_id, item['menu_item_id'], item['quantity']))
            
            connection.commit()
            
            total_amount = sum(float(str(item['price'])) * item['quantity'] for item in cart)
            order_details = {
                'order_id': order_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'delivery_address': customer_address,
                'phone': customer_phone,  # Include phone number in order details
                'items': cart.copy(),
                'total': total_amount
            }
            
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
            order_details = {
                'customer_name': request.form['name'],
                'customer_email': request.form['email'],
                'delivery_address': request.form['address'],
                'phone': request.form.get('phone', ''),
                'items': cart.copy(),
                'total': sum(float(str(item['price'])) * item['quantity'] for item in cart)
            }
            cart.clear()
            return render_template('order_confirmation.html', order=order_details, cart_count=len(cart))
    
    # Check if cart is empty
    if not cart:
        return redirect(url_for('index'))
    
    total = sum(float(str(item['price'])) * item['quantity'] for item in cart)
    return render_template('checkout.html', total=total, cart_count=len(cart))

@app.route('/customers')
def customers():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    # Fetch unique customers by selecting distinct emails
    cursor.execute("""
        SELECT MIN(customer_id) as customer_id, name, email, address
        FROM customers
        GROUP BY email, name, address
        ORDER BY MIN(customer_id)
    """)
    db_customers = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('customers.html', customers=db_customers, cart_count=len(cart))

@app.route('/drivers')
def drivers():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM drivers")
    db_drivers = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('drivers.html', drivers=db_drivers, cart_count=len(cart))

@app.route('/orders')
def orders():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(operation="""
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