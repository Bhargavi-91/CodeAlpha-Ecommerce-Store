from decimal import Decimal
from .models import Product

def get_cart(request):
    return request.session.get("cart", {})

def cart_details(request):
    cart = get_cart(request)
    rows = []
    total = Decimal("0.00")
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
        except (Product.DoesNotExist, ValueError):
            continue
        quantity = max(1, int(quantity))
        line_total = product.price * quantity
        rows.append({"product": product, "quantity": quantity, "line_total": line_total})
        total += line_total
    return rows, total
