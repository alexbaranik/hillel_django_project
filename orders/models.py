from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Case, When, Sum, F
from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import DiscountTypes


class Discount(PKMixin):
    amount = models.PositiveSmallIntegerField(
        default=0
    )
    code = models.CharField(
        max_length=32
    )
    is_active = models.BooleanField(
        default=True
        )
    discount_type = models.PositiveIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )

    def __str__(self) -> str:
        return f'{self.amount} | {self.code}'


class Order(LifecycleModelMixin, PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # products = models.ManyToManyField("products.Product")
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_ordered = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user} | {self.total_amount}'

    # def get_total_amount(self):
    #     if self.discount:
    #         if self.discount.discount_type == DiscountTypes.VALUE:
    #             return self.total_amount - Decimal(
    #                 self.discount.amount).quantize(Decimal('1.00'))
    #         else:
    #             return self.total_amount - Decimal(
    #                     self.total_amount / 100 * self.discount.amount
    #                     ).quantize(Decimal('1.00'))
    #     return self.total_amount

    def get_total_amount(self):
        return self.items.annotate(
            full_price=F('product__price') * F('quantity')
        ).aggregate(
            total_amount=Case(
                When(
                    order__discount__discount_type=DiscountTypes.VALUE,
                    then=Sum('full_price') - F('order__discount__amount')
                ),
                When(
                    order__discount__discount_type=DiscountTypes.PERCENT,
                    then=Sum('full_price') - (
                            Sum('full_price'
                                ) * F('order__discount__amount') / 100
                    )
                ),
                default=Sum('full_price'),
                output_field=models.DecimalField()
            )
        ).get('total_amount') or 0


class OrderItems(PKMixin):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "products.Product",
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
        )
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
