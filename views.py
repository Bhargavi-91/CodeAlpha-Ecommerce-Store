from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .cart import cart_details, get_cart
from .forms import CheckoutForm, RegisterForm
from .models import Order, OrderItem, Product

def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "store/product_detail.html", {"product": product})

def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("home")
    product = get_object_or_404(Product, pk=product_id)
    cart = get_cart(request).copy()
    key = str(product.id)
    current = int(cart.get(key, 0))
    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
    elif current + 1 > product.stock:
        messages.error(request, "Sorry, there is not enough stock.")
    else:
        cart[key] = current + 1
        request.session["cart"] = cart
        messages.success(request, f"{product.name} added to your cart.")
    return redirect("cart")

def cart_view(request):
    rows, total = cart_details(request)
    return render(request, "store/cart.html", {"rows": rows, "total": total})

def update_cart(request, product_id):
    if request.method != "POST":
        return redirect("cart")
    cart = get_cart(request).copy()
    key = str(product_id)
    product = get_object_or_404(Product, pk=product_id)
    try:
        quantity = int(request.POST.get("quantity", "1"))
    except ValueError:
        quantity = 1
    if quantity <= 0:
        cart.pop(key, None)
    elif quantity <= product.stock:
        cart[key] = quantity
    else:
        messages.error(request, f"Only {product.stock} item(s) are available for {product.name}.")
    request.session["cart"] = cart
    return redirect("cart")

def remove_from_cart(request, product_id):
    if request.method == "POST":
        cart = get_cart(request).copy()
        cart.pop(str(product_id), None)
        request.session["cart"] = cart
    return redirect("cart")

@login_required
def checkout(request):
    rows, total = cart_details(request)
    if not rows:
        messages.error(request, "Your cart is empty.")
        return redirect("home")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Recheck stock at order time.
                for row in rows:
                    product = Product.objects.select_for_update().get(pk=row["product"].pk)
                    if row["quantity"] > product.stock:
                        messages.error(request, f"Not enough stock for {product.name}. Please update your cart.")
                        return redirect("cart")
                order = Order.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data["full_name"],
                    phone=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                    total=total,
                )
                for row in rows:
                    product = Product.objects.get(pk=row["product"].pk)
                    quantity = row["quantity"]
                    OrderItem.objects.create(
                        order=order, product=product, quantity=quantity,
                        price_at_purchase=product.price,
                    )
                    product.stock -= quantity
                    product.save(update_fields=["stock"])
            request.session["cart"] = {}
            return render(request, "store/order_success.html", {"order": order})
    else:
        form = CheckoutForm(initial={"full_name": request.user.get_full_name() or request.user.username})
    return render(request, "store/checkout.html", {"form": form, "rows": rows, "total": total})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "store/register.html", {"form": form})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "store/my_orders.html", {"orders": orders})
