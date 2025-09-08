# Deployment Guide

## GitHub Deployment Steps

### 1. Initialize Git Repository
```bash
cd "c:\Users\saiki\OneDrive\Desktop\SAI\Projects\Shiny\Ecommerce"
git init
git add .
git commit -m "Initial commit: Shiny E-Commerce Application"
```

### 2. Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `shiny-ecommerce` or your preferred name
3. Don't initialize with README (we already have one)

### 3. Connect Local Repository to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 4. Deploy to GitHub Pages (Optional)
For static hosting, you can use GitHub Pages, but since this is a Python Shiny app, you'll need a Python hosting service.

## Alternative Deployment Options

### 1. Heroku
Create a `Procfile`:
```
web: python app.py
```

### 2. Railway
Create a `railway.toml`:
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python app.py"
```

### 3. Render
Create a `render.yaml`:
```yaml
services:
  - type: web
    name: shiny-ecommerce
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
```

## Environment Variables
For production deployment, set these environment variables:
- `SMTP_SERVER`: Your SMTP server
- `SMTP_PORT`: SMTP port (usually 587)
- `SENDER_EMAIL`: Your email address
- `SENDER_PASSWORD`: Your email app password

## Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:8000`