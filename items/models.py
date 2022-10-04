# from pyexpat import model
from os import path
from django.db import models
from django.core.validators import MinValueValidator

from shop.mixins.models_mixins import PKMixin


def upload_image(instance, filename):
    _name, extension = path.splitext(filename)
    return f'images/{instance.__class__.__name__.lower()}/'\
            f'{instance.pk}/image{extension}'

class Item(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image)
    category = models.ForeignKey(
        "items.Category",
        on_delete=models.CASCADE
    )


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image)


class Product(PKMixin):
    price = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    scu = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    items = models.ManyToManyField(Item)


class Discount(models.Model):
    # DISCOUNT = (
    #     (0, 'В деньгах'),
    #     (1, 'Проценты'),
    # )

    amount = models.PositiveIntegerField()
    code = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    discount_type = models.PositiveIntegerField(
        choices=((0, 'В деньгах'), (1, 'Проценты'),)
    )
