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

# Custom CSS for modern styling
custom_css = ui.tags.style("""
    /* Global Styles */
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin: 20px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Header Styling */
    .main-title {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Sidebar Styling */
    .sidebar {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 5px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        color: white;
        min-width: 300px;
    }
    
    .sidebar h4 {
        color: white;
        font-weight: bold;
        margin-bottom: 25px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        font-size: 1.3em;
    }
    
    .sidebar .form-group {
        margin-bottom: 20px;
    }
    
    .sidebar .form-group label {
        color: white;
        font-weight: 500;
        margin-bottom: 8px;
        display: block;
        font-size: 1.05em;
    }
    
    .sidebar .form-control {
        border-radius: 12px;
        border: none;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
        padding: 12px 15px;
        width: 100%;
    }
    
    .sidebar .form-control:focus {
        background: white;
        box-shadow: 0 0 15px rgba(255,255,255,0.5);
        transform: scale(1.02);
    }
    
    /* Product Cards */
    .product-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: none;
        border-radius: 20px;
        padding: 25px;
        margin: 15px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .product-card:hover::before {
        left: 100%;
    }
    
    .product-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .product-card img {
        border-radius: 15px;
        transition: transform 0.3s ease;
    }
    
    .product-card:hover img {
        transform: scale(1.05);
    }
    
    .product-card h5 {
        color: #2c3e50;
        font-weight: bold;
        margin: 15px 0 10px 0;
    }
    
    .product-card p {
        color: #7f8c8d;
        margin: 5px 0;
    }
    
    /* Buttons */
    .btn {
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        border: none;
        position: relative;
        overflow: hidden;
    }
    
    .btn-primary {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
    }
    
    .btn-primary:hover {
        background: linear-gradient(45deg, #764ba2, #667eea);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    
    .btn-success {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        color: white;
    }
    
    .btn-success:hover {
        background: linear-gradient(45deg, #a8e6cf, #56ab2f);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(86, 171, 47, 0.4);
    }
    
    .btn-warning {
        background: linear-gradient(45deg, #f093fb, #f5576c);
        color: white;
    }
    
    .btn-warning:hover {
        background: linear-gradient(45deg, #f5576c, #f093fb);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(245, 87, 108, 0.4);
    }
    
    .btn-danger {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white;
    }
    
    .btn-danger:hover {
        background: linear-gradient(45deg, #ff4b2b, #ff416c);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(255, 65, 108, 0.4);
    }
    
    /* Navigation Tabs */
    .nav-tabs {
        border: none;
        margin-bottom: 30px;
    }
    
    .nav-tabs .nav-link {
        border: none;
        border-radius: 25px;
        margin: 0 5px;
        padding: 12px 25px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .nav-tabs .nav-link:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    .nav-tabs .nav-link.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    /* Cart Section */
    .cart-section {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .cart-item {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    
    .cart-item:hover {
        transform: translateX(5px);
    }
    
    /* Form Styling */
    .form-control {
        border-radius: 15px;
        border: 2px solid #e9ecef;
        padding: 12px 20px;
        transition: all 0.3s ease;
        background: rgba(255,255,255,0.9);
    }
    
    .form-control:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
        transform: scale(1.02);
    }
    
    /* Order Cards */
    .order-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .order-card:hover {
        transform: translateY(-5px);
    }
    
    /* Animations */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .product-card {
            margin: 10px 5px;
            padding: 15px;
        }
        
        .main-container {
            margin: 10px;
            padding: 20px;
        }
    }
    
    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
""")

# Login UI
login_ui = ui.page_fluid(
    custom_css,
    ui.div(
        ui.div(
            ui.div(
                ui.h1("🛍️ ShinyCommerce", class_="main-title", style="margin-bottom: 10px;"),
                ui.p("Welcome to the future of shopping", style="text-align: center; color: #7f8c8d; font-size: 1.1em; margin-bottom: 30px;"),
                style="text-align: center; margin-bottom: 40px;"
            ),
            ui.div(
                ui.h3("🔐 Login", style="text-align: center; color: #2c3e50; margin-bottom: 25px;"),
                ui.input_text("email", "📧 Email:", placeholder="Enter your email address"),
                ui.div(
                    ui.output_ui("email_verify_button"),
                    style="margin-top: 15px;"
                ),
                ui.output_ui("email_otp_section"),
                ui.br(),
                ui.div(
                    ui.h5("🎯 Demo Accounts:", style="color: #2c3e50; margin-bottom: 10px;"),
                    ui.div(
                        ui.span("👨💼 admin@demo.com", style="display: block; margin: 5px 0; color: #3498db;"),
                        ui.span("👤 user@demo.com", style="display: block; margin: 5px 0; color: #27ae60;"),
                        ui.span("🎆 demo@demo.com", style="display: block; margin: 5px 0; color: #e74c3c;"),
                    ),
                    style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 20px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 20px 0;"
                ),
                ui.output_ui("login_message"),
                style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 40px; border-radius: 25px; box-shadow: 0 25px 50px rgba(0,0,0,0.15); max-width: 450px; margin: 0 auto; animation: fadeInUp 0.8s ease-out;"
            ),
            style="min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; padding: 20px;"
        )
    )
)

# Main store UI
store_ui = ui.page_fluid(
    custom_css,
    ui.div(
        ui.h1("🛍️ ShinyCommerce", class_="main-title"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.div(
                    ui.h4("🎯 Filters", style="color: white; text-align: center; margin-bottom: 30px;"),
                    ui.div(
                        ui.input_select("category_filter", "📂 Category:",
                                      choices=['All'] + list(products['category'].unique()),
                                      selected="All"),
                        style="margin-bottom: 20px;"
                    ),
                    ui.div(
                        ui.input_slider("price_range", "💰 Price Range ($):", 
                                      min=int(products['price'].min()), 
                                      max=int(products['price'].max()),
                                      value=[10, 500]),
                        style="margin-bottom: 20px;"
                    ),
                    ui.div(
                        ui.input_numeric("min_rating", "⭐ Min Rating:", value=3.0, min=1.0, max=5.0, step=0.1),
                        style="margin-bottom: 25px;"
                    ),
                    ui.hr(style="border-color: rgba(255,255,255,0.3); margin: 20px 0;"),
                    ui.output_ui("cart_title"),
                    ui.output_ui("cart_summary"),
                    class_="sidebar"
                ),
                width=350
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
        class_="main-container"
    ),
    ui.div(
        ui.input_action_button("logout_btn", "😪 Logout", class_="btn-danger btn-sm", style="position: fixed; top: 20px; right: 20px; z-index: 1000; border-radius: 25px; padding: 10px 20px; font-weight: 600;"),
        ui.output_ui("current_user", style="position: fixed; top: 20px; left: 20px; z-index: 1000; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 10px 20px; border-radius: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); font-weight: 600;")
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
            return ui.span(f"👤 Welcome, {logged_in_user()}!", style="color: #2c3e50;")
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
                ui.img(src=product['image'], style="width: 100%; height: 180px; object-fit: cover; border-radius: 15px; margin-bottom: 15px;"),
                ui.h5(product['name'], style="color: #2c3e50; font-weight: bold;"),
                ui.p(f"📂 {product['category']}", style="color: #7f8c8d; font-size: 0.9em;"),
                ui.p(f"💰 ${product['price']}", style="color: #27ae60; font-weight: bold; font-size: 1.1em;"),
                ui.p(f"{'⭐' * int(product['rating'])} ({product['rating']})", style="color: #f39c12;"),
                ui.p(f"📦 {product['stock']} in stock", class_=stock_color, style="font-size: 0.9em;"),
                ui.div(cart_controls, style="margin-top: 15px;"),
                class_="product-card"
            )
            products_ui.append(ui.column(4, product_card))
        
        return ui.div(*[ui.row(*products_ui[i:i+3]) for i in range(0, len(products_ui), 3)])
    
    @render.ui
    def cart_title():
        cart_items = cart()
        total_items = len(cart_items)
        return ui.h4(f"🛍️ Cart ({total_items})", style="color: white; text-align: center; margin-bottom: 20px;")
    
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
            ui.div(
                ui.p(f"📦 Items: {unique_items}", style="color: white; margin: 8px 0; font-size: 1.1em;"),
                ui.p(f"🔢 Qty: {total_quantity}", style="color: white; margin: 8px 0; font-size: 1.1em;"),
                ui.p(f"💰 ${total_price:.2f}", style="color: white; font-weight: bold; font-size: 1.3em; margin: 12px 0;"),
                style="background: rgba(255,255,255,0.25); padding: 25px 20px; border-radius: 15px; backdrop-filter: blur(8px); border: 2px solid rgba(255,255,255,0.1);"
            )
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
                            ui.h5(item['name'], style="color: #2c3e50; margin-bottom: 10px;"),
                            ui.p(f"💰 ${item['price']} each", style="color: #27ae60; font-weight: 500;"),
                            ui.p(f"🔢 Quantity: {item['quantity']}", style="color: #7f8c8d;"),
                            ui.p(f"💵 Subtotal: ${subtotal:.2f}", style="color: #e74c3c; font-weight: bold;"),
                            ui.p(f"📂 {item['category']}", style="color: #9b59b6; font-size: 0.9em;")
                        ),
                        ui.column(4,
                            ui.div(
                                ui.input_action_button(f"remove_{item_id}", "➖ Remove One", 
                                                     class_="btn-warning btn-sm mb-2", style="width: 100%;"),
                                ui.input_action_button(f"remove_all_{item_id}", "🗑️ Remove All", 
                                                     class_="btn-danger btn-sm", style="width: 100%;"),
                                style="text-align: center;"
                            )
                        )
                    ),
                    class_="cart-item"
                )
            )
        
        cart_ui.append(
            ui.div(
                ui.h3(f"💰 Total: ${total:.2f}", style="text-align: center; color: #2c3e50; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1);")
            )
        )
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
                ui.div(
                    ui.h4(f"🛍️ Order #{len(order_history) - i + 1}", style="color: #2c3e50; margin-bottom: 15px;"),
                    ui.p(f"📅 {order['date']}", style="color: #7f8c8d; font-size: 0.9em;"),
                    ui.p(f"👤 {order['address']['name']}", style="color: #34495e; font-weight: 500;"),
                    ui.p(f"📍 {order['address']['full_address']}", style="color: #7f8c8d;"),
                    ui.p(f"📞 {order['address']['phone']}", style="color: #7f8c8d;"),
                    ui.h5("📦 Items:", style="color: #2c3e50; margin: 15px 0 10px 0;"),
                    *order_items,
                    ui.div(
                        ui.h5(f"💰 Total: ${total:.2f}", style="color: #27ae60; font-weight: bold;"),
                        ui.span(f"📦 {order['status']}", style="background: #3498db; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8em;"),
                        style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;"
                    ),
                    class_="order-card"
                )
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
            ui.div(
                ui.h4("🚚 Shipping Address", style="color: #2c3e50; text-align: center; margin-bottom: 25px;"),
                class_="cart-section"
            ),
            ui.row(
                ui.column(6, ui.input_text("full_name", "Full Name:", placeholder="Enter your full name")),
                ui.column(6, ui.input_text("phone", "Phone:", placeholder="Enter phone number"))
            ),
            ui.input_text("address", "Address:", placeholder="Enter street address"),
            ui.row(
                ui.column(4, ui.input_text("city", "City:", placeholder="City")),
                ui.column(4, ui.input_text("state", "State:", placeholder="State")),
                ui.column(4, ui.input_text("zipcode", "ZIP Code:", placeholder="ZIP code"))
            ),
            ui.br(),
            ui.div(
                ui.row(
                    ui.column(6, ui.input_action_button("clear_cart", "🗑️ Clear Cart", class_="btn-warning", style="width: 100%; padding: 15px; font-size: 1.1em;")),
                    ui.column(6, ui.input_action_button("place_order", "🛒 Place Order", class_="btn-success", style="width: 100%; padding: 15px; font-size: 1.1em;"))
                ),
                style="margin-top: 30px;"
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