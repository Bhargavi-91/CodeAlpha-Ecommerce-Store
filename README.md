# BrightCart — CodeAlpha E-commerce Store

A beginner-friendly full-stack e-commerce project built with HTML, CSS, JavaScript-compatible browser pages, Python, Django, and SQLite.

## Features
- Product listing and product detail pages
- Add to cart, update quantities, remove items
- User registration, login, logout
- Checkout form and order processing
- SQLite database for products, users, orders, and order items
- Django admin to manage products and orders
- Responsive design

> This is a learning/demo project. It does not collect real payments. Do not deploy it publicly without reviewing security settings.

## Windows setup

Open this folder in VS Code. In VS Code, choose **Terminal → New Terminal**.

### 1. Create and activate a virtual environment

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt terminal instead and run:

```bat
.venv\Scripts\activate.bat
```

### 2. Install Django

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Create the database tables

```bash
python manage.py makemigrations store
python manage.py migrate
```

### 4. Create an admin account

```bash
python manage.py createsuperuser
```

Follow the prompts to create your username and password.

### 5. Run the website

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Add sample products

1. Open http://127.0.0.1:8000/admin/
2. Log in with the superuser account you created.
3. Under **Store**, choose **Products → Add product**.
4. Add a name, description, price, and stock quantity. Image URL is optional.
5. Save and return to the storefront at http://127.0.0.1:8000/.

Add at least 3 products for your demo.

## Main URLs
- Store: `/`
- Cart: `/cart/`
- Register: `/register/`
- Login: `/login/`
- My orders: `/orders/`
- Admin: `/admin/`

## GitHub submission

After testing, create a repository on GitHub and follow GitHub's instructions to upload this project. Do not upload passwords or real customer data. The local SQLite database file (`db.sqlite3`) is not necessary for submission.

## Before submitting
- Test add/update/remove cart.
- Create a user and place a demo order.
- Confirm the order appears in **My orders**.
- Add screenshots to your README if possible.
- Record a short video explaining the pages and features.
- Follow the exact CodeAlpha submission form and LinkedIn instructions provided by your internship coordinator.
