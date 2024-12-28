from flask import Flask, render_template_string, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session to store cart

# Sample product data (this could be dynamic or from a database)
products = [
    {'id': 1, 'name': 'Product 1', 'price': 100, 'description': 'This is a great product.'},
    {'id': 2, 'name': 'Product 2', 'price': 150, 'description': 'This is another great product.'},
    {'id': 3, 'name': 'Product 3', 'price': 200, 'description': 'Yet another awesome product.'}
]

# Inline CSS styles
css = """
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        color: #333;
        margin: 0;
        padding: 0;
    }
    h1, h2 {
        color: #444;
    }
    .container {
        width: 80%;
        margin: 0 auto;
    }
    .product {
        background-color: white;
        padding: 20px;
        margin: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .product h3 {
        color: #007BFF;
    }
    .product p {
        margin-bottom: 10px;
    }
    button, a {
        background-color: #007BFF;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        text-decoration: none;
    }
    button:hover, a:hover {
        background-color: #0056b3;
    }
    .cart-items {
        list-style-type: none;
        padding: 0;
    }
    .cart-items li {
        background-color: #fff;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .cart-summary {
        margin-top: 20px;
        font-size: 18px;
    }
    .checkout-form input {
        margin: 5px 0;
        padding: 10px;
        width: 100%;
    }
    .checkout-form button {
        width: 100%;
    }
"""

# Home page route
@app.route('/')
def index():
    product_list_html = ""
    for product in products:
        product_list_html += f"""
            <div class="product">
                <h3>{product['name']}</h3>
                <p>{product['description']}</p>
                <p>Price: ${product['price']}</p>
                <a href="{url_for('add_to_cart', product_id=product['id'])}">Add to Cart</a>
            </div>
        """

    return render_template_string(f"""
        <html>
        <head><title>Simple E-Commerce</title><style>{css}</style></head>
        <body>
            <div class="container">
                <h1>Welcome to Our Simple Store</h1>
                <h2>Products</h2>
                <div>{product_list_html}</div>
                <br>
                <a href="{url_for('cart')}">Go to Cart</a>
            </div>
        </body>
        </html>
    """)

# Add a product to the shopping cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Initialize cart if not present in the session
    if 'cart' not in session:
        session['cart'] = []

    # Find the product and add it to the cart
    product = next((prod for prod in products if prod['id'] == product_id), None)
    if product:
        session['cart'].append(product)

    return redirect(url_for('cart'))

# View the shopping cart
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)

    # Generate HTML for the cart items
    cart_items_html = ""
    if cart_items:
        for item in cart_items:
            cart_items_html += f"<li>{item['name']} - ${item['price']}</li>"

        cart_summary_html = f"""
            <div class="cart-summary">
                <h3>Total: ${total_price}</h3>
                <a href="{url_for('checkout')}">Proceed to Checkout</a>
            </div>
        """
    else:
        cart_items_html = "<p>Your cart is empty!</p>"
        cart_summary_html = ""

    return render_template_string(f"""
        <html>
        <head><title>Your Cart</title><style>{css}</style></head>
        <body>
            <div class="container">
                <h1>Your Shopping Cart</h1>
                <ul class="cart-items">
                    {cart_items_html}
                </ul>
                {cart_summary_html}
                <br>
                <a href="{url_for('index')}">Back to Shop</a>
            </div>
        </body>
        </html>
    """)

# Checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        session.pop('cart', None)  # Clear the cart after successful checkout
        return render_template_string(f"""
            <html>
            <head><title>Checkout</title><style>{css}</style></head>
            <body>
                <div class="container">
                    <h1>Checkout Successful</h1>
                    <p>Thank you for your purchase!</p>
                    <a href="{url_for('index')}">Back to Shop</a>
                </div>
            </body>
            </html>
        """)

    return render_template_string(f"""
        <html>
        <head><title>Checkout</title><style>{css}</style></head>
        <body>
            <div class="container">
                <h1>Checkout</h1>
                <form method="POST" class="checkout-form">
                    <label>Name:</label>
                    <input type="text" name="name" required><br>
                    <label>Shipping Address:</label>
                    <input type="text" name="address" required><br><br>
                    <button type="submit">Complete Purchase</button>
                </form>
                <br>
                <a href="{url_for('cart')}">Go back to Cart</a>
            </div>
        </body>
        </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)
