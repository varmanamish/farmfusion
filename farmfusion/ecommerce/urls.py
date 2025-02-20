from django.urls import path
from .views import shop,add_to_cart,view_cart,checkout

urlpatterns = [
    path('', shop, name='shop'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path("checkout/", checkout, name="checkout")
]
