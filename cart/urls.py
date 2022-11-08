from django.urls import path
from cart.views import cart_add, cart_detail, cart_remove


urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<uuid:product_id>/', cart_add, name='cart_add'),
    path('remove/<uuid:product_id>/', cart_remove, name='cart_remove'),
]
