from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem

@login_required
def shop(request):
    # Fetch all products from the Product model
    products = Product.objects.all()
    
    # Fetch the user's orders (if any)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Render the shop template, passing both products and orders
    return render(request, 'ecommerce/shop.html', {'products': products, 'orders': orders})


def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))

        # Get the product
        product = Product.objects.get(id=product_id)

        # Initialize the session cart if it doesn't exist
        cart = request.session.get("cart", {})

        if product_id in cart:
            cart[product_id]["quantity"] += quantity  # Update quantity
        else:
            cart[product_id] = {
                "name": product.name,
                "cost": float(product.cost),
                "quantity": quantity,
            }

        request.session["cart"] = cart  # Save cart to session
        return JsonResponse({"message": "Added to cart", "cart_count": len(cart)})

def view_cart(request):
    cart = request.session.get("cart", {})
    total = sum(item["cost"] * item["quantity"] for item in cart.values())
    return render(request, "ecommerce/cart.html", {"cart": cart, "total": total})



@login_required
def checkout(request):
    if request.method == "POST":
        user = request.user  # Get the logged-in user
        cart = request.session.get("cart", {})

        if not cart:
            return JsonResponse({"message": "Cart is empty!"}, status=400)

        total_amount = sum(float(item["cost"]) * int(item["quantity"]) for item in cart.values())

        # Create a new Order instance
        order = Order.objects.create(user=user, total_amount=total_amount)

        # Create OrderItems
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=item["cost"],
            )

        # Clear the session cart
        request.session["cart"] = {}

        return JsonResponse({"message": "Checkout successful!", "order_id": order.id})
    
    return JsonResponse({"message": "Invalid request"}, status=400)

@login_required
def order_history(request):
    # Fetch all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Pass the orders and order items to the template
    return render(request, 'ecommerce/shop.html/', {'orders': orders})
