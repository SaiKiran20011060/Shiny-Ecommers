# Shiny E-Commerce Application -- https://01992a0e-dc7c-e0ad-817e-c126b6933dc8.share.connect.posit.cloud/

A Demo modern e-commerce web application built with Python Shiny, featuring user authentication, shopping cart functionality, order management, and analytics dashboard.

## Features

- **User Authentication**: Email-based OTP verification system
- **Product Catalog**: Browse products by category with filtering options
- **Shopping Cart**: Add, remove, and manage items in your cart
- **Order Management**: Place orders and track order history
- **Analytics Dashboard**: View sales analytics and product insights
- **Responsive Design**: Mobile-friendly interface

## Demo Credentials

For testing purposes, you can use these demo emails:
- admin@demo.com
- user@demo.com  
- demo@demo.com

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SaiKiran20011060/Shiny-Ecommers.git
cd Shiny-Ecommers
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to the URL shown in the terminal (typically `http://127.0.0.1:8000`)

## Project Structure

```
Shiny-Ecommers/
├── shinyecomm.py          # Main application logic
├── app.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── render.yaml           # Render.com deployment config
├── .github/workflows/    # GitHub Actions
├── README.md             # Project documentation
└── .gitignore           # Git ignore file
```

## Technologies Used

- **Python Shiny**: Web framework for building interactive applications
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib**: Data visualization and plotting

## Usage

1. **Login**: Enter your email and verify with OTP
2. **Browse Products**: Use filters to find products by category, price, and rating
3. **Shopping**: Add items to cart and manage quantities
4. **Checkout**: Enter shipping details and place orders
5. **Analytics**: View sales data and product insights

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Deployment

### Local Development
```bash
python app.py
```

### Docker Deployment
```bash
docker build -t shiny-ecommerce .
docker run -p 8000:8000 shiny-ecommerce
```

### Cloud Deployment
- **Render.com**: Connect your GitHub repository and deploy using `render.yaml`
- **Heroku**: Use the included `Dockerfile` for container deployment
- **Railway**: Connect GitHub repo for automatic deployment

## Contact

For questions or support, please open an issue on GitHub.
