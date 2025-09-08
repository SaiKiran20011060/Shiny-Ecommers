from shiny import App, reactive, render, ui
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
try:
    from email_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
except ImportError:
    # Fallback values if config file doesn't exist
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "your-email@gmail.com"
    SENDER_PASSWORD = "your-app-password"

# E-commerce data with real products
np.random.seed(42)
real_products = {
    'Electronics': [('iPhone 14', 'https://d1eh9yux7w8iql.cloudfront.net/product_images/781085_ac40df2e-8547-4c88-91e6-9437ced8796d.jpg'), 
                   ('Samsung Galaxy S23', 'https://via.placeholder.com/200x150/28a745/ffffff?text=Galaxy+S23'),
                   ('MacBook Pro', 'https://via.placeholder.com/200x150/6c757d/ffffff?text=MacBook+Pro'),
                   ('Dell XPS 13', 'https://via.placeholder.com/200x150/17a2b8/ffffff?text=Dell+XPS'),
                   ('iPad Air', 'https://via.placeholder.com/200x150/ffc107/000000?text=iPad+Air'),
                   ('AirPods Pro', 'https://via.placeholder.com/200x150/dc3545/ffffff?text=AirPods'),
                   ('Sony Headphones', 'https://via.placeholder.com/200x150/6f42c1/ffffff?text=Headphones'),
                   ('Nintendo Switch', 'https://via.placeholder.com/200x150/fd7e14/ffffff?text=Switch'),
                   ('Smart TV 55"', 'https://via.placeholder.com/200x150/20c997/ffffff?text=Smart+TV'),
                   ('Gaming Mouse', 'https://via.placeholder.com/200x150/e83e8c/ffffff?text=Mouse')],
    'Clothing': [('Nike Air Max', 'https://via.placeholder.com/200x150/007bff/ffffff?text=Nike+Shoes'),
                ('Levi\'s Jeans', 'https://via.placeholder.com/200x150/6c757d/ffffff?text=Jeans'),
                ('Adidas T-Shirt', 'https://via.placeholder.com/200x150/28a745/ffffff?text=T-Shirt'),
                ('Winter Jacket', 'https://via.placeholder.com/200x150/17a2b8/ffffff?text=Jacket'),
                ('Summer Dress', 'https://via.placeholder.com/200x150/ffc107/000000?text=Dress'),
                ('Formal Shirt', 'https://via.placeholder.com/200x150/dc3545/ffffff?text=Shirt'),
                ('Sneakers', 'https://via.placeholder.com/200x150/6f42c1/ffffff?text=Sneakers'),
                ('Baseball Cap', 'https://via.placeholder.com/200x150/fd7e14/ffffff?text=Cap'),
                ('Hoodie', 'https://via.placeholder.com/200x150/20c997/ffffff?text=Hoodie'),
                ('Sunglasses', 'https://via.placeholder.com/200x150/e83e8c/ffffff?text=Sunglasses')],
    'Books': [('Python Programming', 'https://via.placeholder.com/200x150/007bff/ffffff?text=Python+Book'),
             ('Data Science Guide', 'https://via.placeholder.com/200x150/28a745/ffffff?text=Data+Science'),
             ('Web Development', 'https://via.placeholder.com/200x150/6c757d/ffffff?text=Web+Dev'),
             ('Machine Learning', 'https://via.placeholder.com/200x150/17a2b8/ffffff?text=ML+Book'),
             ('JavaScript Guide', 'https://via.placeholder.com/200x150/ffc107/000000?text=JavaScript'),
             ('Design Patterns', 'https://via.placeholder.com/200x150/dc3545/ffffff?text=Design'),
             ('Algorithm Book', 'https://via.placeholder.com/200x150/6f42c1/ffffff?text=Algorithms'),
             ('React Handbook', 'https://via.placeholder.com/200x150/fd7e14/ffffff?text=React'),
             ('AI Fundamentals', 'https://via.placeholder.com/200x150/20c997/ffffff?text=AI+Book'),
             ('Cloud Computing', 'https://via.placeholder.com/200x150/e83e8c/ffffff?text=Cloud')],
    'Home': [('Coffee Maker', 'https://via.placeholder.com/200x150/007bff/ffffff?text=Coffee+Maker'),
            ('Blender', 'https://via.placeholder.com/200x150/28a745/ffffff?text=Blender'),
            ('Vacuum Cleaner', 'https://via.placeholder.com/200x150/6c757d/ffffff?text=Vacuum'),
            ('Air Purifier', 'https://via.placeholder.com/200x150/17a2b8/ffffff?text=Air+Purifier'),
            ('Table Lamp', 'https://via.placeholder.com/200x150/ffc107/000000?text=Lamp'),
            ('Kitchen Scale', 'https://via.placeholder.com/200x150/dc3545/ffffff?text=Scale'),
            ('Microwave', 'https://via.placeholder.com/200x150/6f42c1/ffffff?text=Microwave'),
            ('Toaster', 'https://via.placeholder.com/200x150/fd7e14/ffffff?text=Toaster'),
            ('Plant Pot', 'https://via.placeholder.com/200x150/20c997/ffffff?text=Plant+Pot'),
            ('Candle Set', 'https://via.placeholder.com/200x150/e83e8c/ffffff?text=Candles')],
    'Sports': [('Yoga Mat', 'https://via.placeholder.com/200x150/007bff/ffffff?text=Yoga+Mat'),
              ('Dumbbells', 'https://via.placeholder.com/200x150/28a745/ffffff?text=Dumbbells'),
              ('Basketball', 'https://via.placeholder.com/200x150/6c757d/ffffff?text=Basketball'),
              ('Tennis Racket', 'https://via.placeholder.com/200x150/17a2b8/ffffff?text=Tennis'),
              ('Running Shoes', 'https://via.placeholder.com/200x150/ffc107/000000?text=Running+Shoes'),
              ('Water Bottle', 'https://via.placeholder.com/200x150/dc3545/ffffff?text=Water+Bottle'),
              ('Fitness Tracker', 'https://via.placeholder.com/200x150/6f42c1/ffffff?text=Fitness'),
              ('Soccer Ball', 'https://via.placeholder.com/200x150/fd7e14/ffffff?text=Soccer'),
              ('Bicycle', 'https://via.placeholder.com/200x150/20c997/ffffff?text=Bicycle'),
              ('Protein Powder', 'https://via.placeholder.com/200x150/e83e8c/ffffff?text=Protein')]
}

# Create products dataframe
product_data = []
for i, (category, items) in enumerate(real_products.items()):
    for j, (name, image) in enumerate(items):
        product_data.append({
            'id': i * 10 + j + 1,
            'name': name,
            'category': category,
            'image': image
        })

products = pd.DataFrame(product_data)
products['price'] = np.random.uniform(10, 500, len(products)).round(2)
products['stock'] = np.random.randint(0, 100, len(products))
products['rating'] = np.random.uniform(3.0, 5.0, len(products)).round(1)
products['sales'] = np.random.randint(0, 1000, len(products))

# Simple user database (in production, use proper authentication)
USERS = {
    'admin': 'password123',
    'user': 'user123',
    'demo': 'demo'
}

# Login UI
login_ui = ui.page_fluid(
    ui.div(
        ui.div(
            ui.h2("🛍️ E-Commerce Store Login", style="text-align: center; color: #007bff;"),
            ui.br(),
            ui.input_text("email", "Email:", placeholder="Enter your email"),
            ui.div(
                ui.output_ui("email_verify_button"),
                style="margin-top: 5px;"
            ),
            ui.output_ui("email_otp_section"),
            ui.br(),
            ui.div(
                ui.h5("Demo Emails:"),
                ui.p("admin@demo.com | user@demo.com | demo@demo.com"),
                style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border: 1px solid #dee2e6;"
            ),
            ui.output_ui("login_message"),
            style="max-width: 400px; margin: 0 auto; padding: 30px; border: 1px solid #ddd; border-radius: 10px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
        ),
        style="min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; padding: 20px;"
    )
)

# Main store UI
store_ui = ui.page_fluid(
    ui.h1("E-Commerce Store"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("category_filter", "Filter by Category:",
                          choices=['All'] + list(products['category'].unique()),
                          selected="All"),
            ui.input_slider("price_range", "Price Range ($):", 
                          min=int(products['price'].min()), 
                          max=int(products['price'].max()),
                          value=[10, 500]),
            ui.input_numeric("min_rating", "Minimum Rating:", value=3.0, min=1.0, max=5.0, step=0.1),
            ui.hr(),
            ui.output_ui("cart_title"),
            ui.output_ui("cart_summary")
        ),
        ui.navset_tab(
            ui.nav_panel("Products",
                ui.output_ui("product_grid")
            ),
            ui.nav_panel("Cart",
                ui.output_ui("cart_details"),
                ui.br(),
                ui.output_ui("checkout_section")
            ),
            ui.nav_panel("My Orders",
                ui.output_ui("orders_list")
            ),
            ui.nav_panel("Analytics",
                ui.row(
                    ui.column(6, ui.output_plot("sales_by_category")),
                    ui.column(6, ui.output_plot("price_distribution"))
                ),
                ui.row(
                    ui.column(12, ui.output_data_frame("products_table"))
                )
            )
        )
    ),
    ui.div(
        ui.input_action_button("logout_btn", "Logout", class_="btn-outline-secondary btn-sm", style="position: fixed; top: 10px; right: 10px; z-index: 1000;"),
        ui.output_ui("current_user", style="position: fixed; top: 10px; left: 10px; z-index: 1000; background: rgba(255,255,255,0.9); padding: 5px 10px; border-radius: 5px;")
    )
)

app_ui = ui.output_ui("main_ui")

def server(input, output, session):
    # Authentication state
    is_logged_in = reactive.value(False)
    logged_in_user = reactive.value("")
    
    cart = reactive.value([])
    orders = reactive.value([])
    
    # Email OTP verification state
    email_otp_sent = reactive.value(False)
    email_otp_verified = reactive.value(False)
    current_email = reactive.value("")
    generated_email_otp = reactive.value("")
    email_otp_timestamp = reactive.value(0)
    
    @render.ui
    def main_ui():
        if is_logged_in():
            return store_ui
        else:
            return login_ui
    
    @render.ui
    def login_message():
        return ui.div(id="login_msg")
    
    @render.ui
    def current_user():
        if is_logged_in():
            return ui.span(f"👤 Welcome, {logged_in_user()}!", style="font-weight: bold; color: #007bff;")
        return ui.span()
    
    # Email OTP functions
    def generate_email_otp():
        return str(random.randint(100000, 999999))
    
    def send_email_otp(email):
        otp = generate_email_otp()
        generated_email_otp.set(otp)
        email_otp_timestamp.set(time.time())
        
        # Always use demo mode - show OTP in notification
        ui.notification_show(f"Demo Mode: Your OTP is {otp}", type="warning", duration=10)
        print(f"Demo OTP for {email}: {otp}")
        return otp
    
    def is_email_otp_valid(entered_otp):
        if time.time() - email_otp_timestamp() > 300:  # 5 minutes
            return False
        return entered_otp == generated_email_otp()
    
    @render.ui
    def email_verify_button():
        email = input.email() or ""
        
        # Reset states if email changed
        if email != current_email():
            email_otp_sent.set(False)
            email_otp_verified.set(False)
        
        if not email or "@" not in email:
            return ui.input_action_button("send_email_otp", "Send OTP", class_="btn-outline-secondary btn-sm", disabled=True)
        
        if email_otp_verified() and current_email() == email:
            return ui.div(
                ui.span("✅ Email Verified", style="color: #28a745; font-weight: bold;"),
                ui.br(),
                ui.input_action_button("email_login", "Login", class_="btn-success", style="width: 100%; margin-top: 10px;")
            )
        
        return ui.input_action_button("send_email_otp", "Send OTP", class_="btn-primary btn-sm")
    
    @render.ui
    def email_otp_section():
        if not email_otp_sent():
            return ui.div()
        
        if email_otp_sent() and not email_otp_verified():
            return ui.div(
                ui.p("📧 OTP sent to your email!", style="color: #28a745; font-size: 0.9em; margin-top: 5px;"),
                ui.input_text("email_otp_input", "Enter OTP:", placeholder="Enter 6-digit OTP"),
                ui.div(
                    ui.input_action_button("verify_email_otp", "Verify OTP", class_="btn-success btn-sm"),
                    " ",
                    ui.input_action_button("resend_email_otp", "Resend OTP", class_="btn-outline-secondary btn-sm"),
                    style="margin-top: 5px;"
                )
            )
        
        return ui.div()
    
    # Email OTP handlers
    @reactive.effect
    @reactive.event(input.send_email_otp)
    def _():
        email = input.email() or ""
        if email and "@" in email:
            otp = send_email_otp(email)
            current_email.set(email)
            email_otp_sent.set(True)
            email_otp_verified.set(False)
            ui.notification_show(f"OTP sent to {email}! Check your inbox.", type="info")
        else:
            ui.notification_show("Please enter a valid email address!", type="error")
    
    @reactive.effect
    @reactive.event(input.verify_email_otp)
    def _():
        entered_otp = input.email_otp_input() or ""
        if is_email_otp_valid(entered_otp):
            email_otp_verified.set(True)
            ui.notification_show("✅ Email verified!", type="success")
        else:
            ui.notification_show("❌ Invalid or expired OTP!", type="error")
    
    @reactive.effect
    @reactive.event(input.resend_email_otp)
    def _():
        email = current_email()
        if email:
            otp = send_email_otp(email)
            ui.notification_show(f"OTP resent to {email}! Check your inbox.", type="info")
    
    @reactive.effect
    @reactive.event(input.email_login)
    def _():
        if email_otp_verified():
            email = current_email()
            is_logged_in.set(True)
            logged_in_user.set(email)
            ui.notification_show(f"Welcome {email}!", type="success")
        else:
            ui.notification_show("Please verify your email first!", type="error")
    
    @reactive.effect
    @reactive.event(input.logout_btn)
    def handle_logout():
        is_logged_in.set(False)
        logged_in_user.set("")
        cart.set([])  # Clear cart on logout
        ui.notification_show("Logged out successfully!", type="info")
    
    def get_cart_quantity(product_id):
        cart_items = cart()
        return sum(1 for item in cart_items if item['id'] == product_id)
    
    @reactive.calc
    def filtered_products():
        data = products.copy()
        if input.category_filter() != 'All':
            data = data[data['category'] == input.category_filter()]
        data = data[(data['price'] >= input.price_range()[0]) & (data['price'] <= input.price_range()[1])]
        data = data[data['rating'] >= input.min_rating()]
        return data
    
    @render.ui
    def product_grid():
        data = filtered_products()
        products_ui = []
        
        for _, product in data.iterrows():
            stock_status = "In Stock" if product['stock'] > 0 else "Out of Stock"
            stock_color = "text-success" if product['stock'] > 0 else "text-danger"
            
            cart_qty = get_cart_quantity(product['id'])
            
            if cart_qty > 0:
                cart_controls = ui.div(
                    ui.input_action_button(f"decrease_{product['id']}", "-", 
                                         class_="btn-warning btn-sm", 
                                         style="width: 30px; margin-right: 5px;"),
                    ui.span(f"{cart_qty}", style="margin: 0 10px; font-weight: bold;"),
                    ui.input_action_button(f"increase_{product['id']}", "+", 
                                         class_="btn-success btn-sm", 
                                         style="width: 30px; margin-left: 5px;"),
                    style="display: flex; align-items: center; justify-content: center;"
                )
            else:
                cart_controls = ui.input_action_button(f"add_{product['id']}", "Add to Cart", 
                                                     disabled=product['stock'] == 0,
                                                     class_="btn-primary btn-sm")
            
            product_card = ui.div(
                ui.img(src=product['image'], style="width: 100%; height: 150px; object-fit: cover; border-radius: 5px; margin-bottom: 10px;"),
                ui.h5(product['name']),
                ui.p(f"Category: {product['category']}"),
                ui.p(f"Price: ${product['price']}"),
                ui.p(f"Rating: {'⭐' * int(product['rating'])} ({product['rating']})"),
                ui.p(f"Stock: {product['stock']}", class_=stock_color),
                cart_controls,
                style="border: 1px solid #ddd; padding: 15px; margin: 10px; border-radius: 5px; background-color: #fff;"
            )
            products_ui.append(ui.column(4, product_card))
        
        return ui.div(*[ui.row(*products_ui[i:i+3]) for i in range(0, len(products_ui), 3)])
    
    @render.ui
    def cart_title():
        cart_items = cart()
        total_items = len(cart_items)
        return ui.h4(f"🛍️ Shopping Cart ({total_items})")
    
    @render.ui
    def cart_summary():
        cart_items = cart()
        item_counts = {}
        for item in cart_items:
            if item['id'] in item_counts:
                item_counts[item['id']]['quantity'] += 1
            else:
                item_counts[item['id']] = {
                    'name': item['name'],
                    'price': item['price'],
                    'quantity': 1
                }
        
        total_price = sum(item['price'] * item['quantity'] for item in item_counts.values())
        unique_items = len(item_counts)
        total_quantity = sum(item['quantity'] for item in item_counts.values())
        
        return ui.div(
            ui.p(f"Unique Items: {unique_items}"),
            ui.p(f"Total Quantity: {total_quantity}"),
            ui.p(f"Total: ${total_price:.2f}")
        )
    
    @render.ui
    def cart_details():
        cart_items = cart()
        if not cart_items:
            return ui.p("Your cart is empty")
        
        item_counts = {}
        for item in cart_items:
            if item['id'] in item_counts:
                item_counts[item['id']]['quantity'] += 1
            else:
                item_counts[item['id']] = {
                    'name': item['name'],
                    'price': item['price'],
                    'category': item['category'],
                    'quantity': 1
                }
        
        cart_ui = []
        total = 0
        for item_id, item in item_counts.items():
            subtotal = item['price'] * item['quantity']
            total += subtotal
            cart_ui.append(
                ui.div(
                    ui.row(
                        ui.column(8,
                            ui.h5(item['name']),
                            ui.p(f"Price: ${item['price']} each"),
                            ui.p(f"Quantity: {item['quantity']}"),
                            ui.p(f"Subtotal: ${subtotal:.2f}"),
                            ui.p(f"Category: {item['category']}")
                        ),
                        ui.column(4,
                            ui.input_action_button(f"remove_{item_id}", "Remove One", 
                                                 class_="btn-warning btn-sm mb-2"),
                            ui.br(),
                            ui.input_action_button(f"remove_all_{item_id}", "Remove All", 
                                                 class_="btn-danger btn-sm")
                        )
                    ),
                    ui.hr()
                )
            )
        
        cart_ui.append(ui.h4(f"Total: ${total:.2f}"))
        return ui.div(*cart_ui)
    
    @render.ui
    def orders_list():
        order_history = orders()
        if not order_history:
            return ui.div(
                ui.h3("📦 My Orders"),
                ui.p("No orders placed yet. Start shopping to see your orders here!")
            )
        
        orders_ui = [ui.h3("📦 My Orders")]
        for i, order in enumerate(reversed(order_history), 1):
            order_items = []
            total = 0
            for item in order['items']:
                subtotal = item['price'] * item['quantity']
                total += subtotal
                order_items.append(
                    ui.p(f"• {item['name']} - Qty: {item['quantity']} - ${subtotal:.2f}")
                )
            
            order_card = ui.div(
                ui.h4(f"Order #{len(order_history) - i + 1}"),
                ui.p(f"📅 Date: {order['date']}"),
                ui.p(f"📍 Shipping to: {order['address']['name']}"),
                ui.p(f"📧 Address: {order['address']['full_address']}"),
                ui.p(f"📞 Phone: {order['address']['phone']}"),
                ui.h5("Items:"),
                *order_items,
                ui.h5(f"💰 Total: ${total:.2f}"),
                ui.p(f"📦 Status: {order['status']}"),
                style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; background-color: #f8f9fa;"
            )
            orders_ui.append(order_card)
        
        return ui.div(*orders_ui)
    

    
    @render.ui
    def checkout_section():
        cart_items = cart()
        if not cart_items:
            return ui.div(
                ui.input_action_button("clear_cart", "Clear Cart", class_="btn-warning", disabled=True),
                style="text-align: center;"
            )
        
        return ui.div(
            ui.h4("Shipping Address"),
            ui.row(
                ui.column(6, ui.input_text("full_name", "Full Name:", placeholder="Enter your full name")),
                ui.column(6, ui.tags.div(
                    ui.tags.label("Phone:"),
                    ui.tags.input(
                        type="text", 
                        id="phone-input", 
                        placeholder="Enter 10-digit phone number",
                        style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;",
                        oninput="validatePhoneInput(this, 'phone-error')"
                    ),
                    ui.div(ui.input_text("phone", ""), style="display: none;"),
                    ui.tags.div(
                        ui.tags.span("⚠️ Phone number must be exactly 10 digits!"),
                        ui.tags.button("×", onclick="closePopup('phone-error')", 
                                      style="float: right; background: none; border: none; font-size: 18px; cursor: pointer;"),
                        id="phone-error",
                        style="display: none; background: #f8d7da; color: #721c24; padding: 10px; margin-top: 5px; border-radius: 4px; border: 1px solid #f5c6cb;"
                    )
                ))
            ),
            ui.input_text("address", "Address:", placeholder="Enter street address"),
            ui.row(
                ui.column(4, ui.input_text("city", "City:", placeholder="City")),
                ui.column(4, ui.input_text("state", "State:", placeholder="State")),
                ui.column(4, ui.tags.div(
                    ui.tags.label("ZIP Code:"),
                    ui.tags.input(
                        type="text", 
                        id="zipcode-input", 
                        placeholder="Enter ZIP code",
                        style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;",
                        oninput="validateNumericInput(this, 'zipcode-error')"
                    ),
                    ui.div(ui.input_text("zipcode", ""), style="display: none;"),
                    ui.tags.div(
                        ui.tags.span("⚠️ ZIP code must contain only numbers!"),
                        ui.tags.button("×", onclick="closePopup('zipcode-error')", 
                                      style="float: right; background: none; border: none; font-size: 18px; cursor: pointer;"),
                        id="zipcode-error",
                        style="display: none; background: #f8d7da; color: #721c24; padding: 10px; margin-top: 5px; border-radius: 4px; border: 1px solid #f5c6cb;"
                    )
                ))
            ),
            ui.tags.script("""
                function validateNumericInput(input, errorId) {
                    const value = input.value;
                    const errorDiv = document.getElementById(errorId);
                    
                    // Sync with hidden Shiny input for ZIP code
                    if (input.id === 'zipcode-input') {
                        const hiddenZipcode = document.querySelector('input[id*="zipcode"][style*="display: none"]');
                        if (hiddenZipcode) {
                            hiddenZipcode.value = input.value;
                            hiddenZipcode.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    }
                    
                    if (value && !/^[0-9]*$/.test(value)) {
                        errorDiv.style.display = 'block';
                        input.style.borderColor = '#dc3545';
                    } else {
                        errorDiv.style.display = 'none';
                        input.style.borderColor = '#ccc';
                    }
                    checkFormValidity();
                }
                
                window.syncCustomInputs = function() {
                    const phoneInput = document.getElementById('phone-input');
                    const hiddenPhone = document.querySelector('input[id*="phone"][style*="display: none"]');
                    if (phoneInput && hiddenPhone) {
                        hiddenPhone.value = phoneInput.value;
                        hiddenPhone.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    
                    const zipcodeInput = document.getElementById('zipcode-input');
                    const hiddenZipcode = document.querySelector('input[id*="zipcode"][style*="display: none"]');
                    if (zipcodeInput && hiddenZipcode) {
                        hiddenZipcode.value = zipcodeInput.value;
                        hiddenZipcode.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }
                
                function closePopup(errorId) {
                    const errorDiv = document.getElementById(errorId);
                    const inputId = errorId.replace('-error', '-input');
                    const input = document.getElementById(inputId);
                    
                    errorDiv.style.display = 'none';
                    if (input) {
                        input.style.borderColor = '#ccc';
                    }
                    checkFormValidity();
                }
                
                function validatePhoneInput(input, errorId) {
                    const value = input.value;
                    const errorDiv = document.getElementById(errorId);
                    
                    input.value = value.replace(/[^0-9]/g, '');
                    
                    // Sync with hidden Shiny input
                    const hiddenPhone = document.querySelector('input[id*="phone"][style*="display: none"]');
                    if (hiddenPhone) {
                        hiddenPhone.value = input.value;
                        hiddenPhone.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    
                    if (input.value && (input.value.length !== 10 || !/^[0-9]{10}$/.test(input.value))) {
                        errorDiv.style.display = 'block';
                        input.style.borderColor = '#dc3545';
                    } else {
                        errorDiv.style.display = 'none';
                        input.style.borderColor = '#ccc';
                    }
                    checkFormValidity();
                }
                
                function checkFormValidity() {
                    const fullName = document.querySelector('input[id*="full_name"]')?.value || '';
                    const phone = document.getElementById('phone-input')?.value || '';
                    const address = document.querySelector('input[id*="address"]')?.value || '';
                    const city = document.querySelector('input[id*="city"]')?.value || '';
                    const state = document.querySelector('input[id*="state"]')?.value || '';
                    const zipcode = document.getElementById('zipcode-input')?.value || '';
                    
                    const allFilled = fullName && phone && address && city && state && zipcode;
                    const phoneValid = /^[0-9]{10}$/.test(phone);
                    const zipcodeValid = /^[0-9]+$/.test(zipcode);
                    
                    const placeOrderBtn = document.querySelector('button[id*="place_order"]');
                    if (placeOrderBtn) {
                        if (allFilled && phoneValid && zipcodeValid) {
                            placeOrderBtn.disabled = false;
                            placeOrderBtn.style.opacity = '1';
                        } else {
                            placeOrderBtn.disabled = true;
                            placeOrderBtn.style.opacity = '0.6';
                        }
                    }
                }
                
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(function() {
                        const inputs = document.querySelectorAll('input[id*="full_name"], input[id*="phone"], input[id*="address"], input[id*="city"], input[id*="state"], #zipcode-input');
                        inputs.forEach(input => {
                            input.addEventListener('input', checkFormValidity);
                        });
                        checkFormValidity();
                    }, 500);
                });
            """),
            ui.br(),
            ui.row(
                ui.column(6, ui.input_action_button("clear_cart", "Clear Cart", class_="btn-warning")),
                ui.column(6, ui.input_action_button("place_order", "Place Order", class_="btn-success", disabled=True))
            )
        )
    

    
    @render.plot
    def sales_by_category():
        data = filtered_products()
        category_sales = data.groupby('category')['sales'].sum()
        
        plt.figure(figsize=(10, 6))
        plt.bar(category_sales.index, category_sales.values)
        plt.title("Sales by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt.gcf()
    
    @render.plot
    def price_distribution():
        data = filtered_products()
        
        plt.figure(figsize=(8, 6))
        plt.hist(data['price'], bins=20, edgecolor='black')
        plt.title("Price Distribution")
        plt.xlabel("Price ($)")
        plt.ylabel("Number of Products")
        plt.tight_layout()
        return plt.gcf()
    
    @render.data_frame
    def products_table():
        return filtered_products()[['name', 'category', 'price', 'stock', 'rating', 'sales']]
    
    # Add to cart functionality
    def add_to_cart_handler(product_id):
        @reactive.effect
        @reactive.event(input[f"add_{product_id}"])
        def _():
            product = products[products['id'] == product_id].iloc[0]
            current_cart = list(cart())
            current_cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'category': product['category']
            })
            cart.set(current_cart)
            ui.notification_show(f"Added {product['name']} to cart!", type="success")
    
    for pid in products['id']:
        add_to_cart_handler(pid)
    
    # Increase/decrease cart functionality
    def increase_handler(product_id):
        @reactive.effect
        @reactive.event(input[f"increase_{product_id}"])
        def _():
            product = products[products['id'] == product_id].iloc[0]
            current_cart = list(cart())
            current_cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'category': product['category']
            })
            cart.set(current_cart)
    
    def decrease_handler(product_id):
        @reactive.effect
        @reactive.event(input[f"decrease_{product_id}"])
        def _():
            current_cart = list(cart())
            for i, item in enumerate(current_cart):
                if item['id'] == product_id:
                    current_cart.pop(i)
                    break
            cart.set(current_cart)
    
    for pid in products['id']:
        increase_handler(pid)
        decrease_handler(pid)
    
    # Remove from cart functionality
    def remove_one_handler(product_id):
        @reactive.effect
        @reactive.event(input[f"remove_{product_id}"])
        def _():
            current_cart = list(cart())
            for i, item in enumerate(current_cart):
                if item['id'] == product_id:
                    current_cart.pop(i)
                    break
            cart.set(current_cart)
    
    def remove_all_handler(product_id):
        @reactive.effect
        @reactive.event(input[f"remove_all_{product_id}"])
        def _():
            current_cart = [item for item in cart() if item['id'] != product_id]
            cart.set(current_cart)
    
    for pid in products['id']:
        remove_one_handler(pid)
        remove_all_handler(pid)
    

    
    @reactive.effect
    @reactive.event(input.place_order)
    def _():
        if len(cart()) == 0:
            ui.notification_show("Cart is empty!", type="warning")
            return
        
        phone_val = input.phone() or "1234567890"
        zipcode_val = input.zipcode() or "12345"
        
        if not input.full_name():
            ui.notification_show("Please enter your full name!", type="error")
            return
        
        if not input.address():
            ui.notification_show("Please enter your address!", type="error")
            return
        
        if not input.city():
            ui.notification_show("Please enter your city!", type="error")
            return
        
        if not input.state():
            ui.notification_show("Please enter your state!", type="error")
            return
        
        if len(cart()) > 0:
            cart_items = cart()
            item_counts = {}
            for item in cart_items:
                if item['id'] in item_counts:
                    item_counts[item['id']]['quantity'] += 1
                else:
                    item_counts[item['id']] = {
                        'name': item['name'],
                        'price': item['price'],
                        'category': item['category'],
                        'quantity': 1
                    }
            
            new_order = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'items': list(item_counts.values()),
                'address': {
                    'name': input.full_name(),
                    'phone': phone_val,
                    'full_address': f"{input.address()}, {input.city()}, {input.state()}"
                },
                'status': 'Processing'
            }
            
            current_orders = list(orders())
            current_orders.append(new_order)
            orders.set(current_orders)
            
            cart.set([])
            ui.notification_show("Order placed successfully!", type="success")
        else:
            ui.notification_show("Cart is empty!", type="warning")
    
    @reactive.effect
    @reactive.event(input.clear_cart)
    def _():
        cart.set([])
        ui.notification_show("Cart cleared!", type="info")

app = App(app_ui, server)

