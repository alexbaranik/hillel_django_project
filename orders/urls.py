from django.urls import path
from orders.views import order_create, pay_order


urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('pay/<uuid:order_id>/', pay_order, name='pay_order')
]
