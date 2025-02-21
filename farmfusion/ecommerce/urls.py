from django.urls import path
from .views import shop, add_to_cart, view_cart, checkout, order_history

urlpatterns = [
    path('', shop, name='shop'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path("checkout/", checkout, name="checkout"),
    path('order-history/', order_history, name='order_history'),  # Add this line for order history
]
