from django.contrib import admin
from django.utils.safestring import mark_safe

from orders.models import Order, Discount, OrderItems


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('overall_amount',)
    list_display = ('user', 'total_amount', 'discount', 'created_at',
                    'overall_amount', 'is_paid')
    inlines = [OrderItemsInline]

    def overall_amount(self, instance):
        return mark_safe(instance.get_total_amount())


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('amount', 'code', 'is_active')
