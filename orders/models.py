from django.db import models
from django.contrib.auth import get_user_model

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
        return f'{self.amount} | {self.discount_type}'


class Order(PKMixin):
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
    product = models.ManyToManyField("items.Product")
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.user} | {self.total_amount}'
