from django.contrib import admin

from orders.models import Order, Discount


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'created_at',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('amount', 'code',)
