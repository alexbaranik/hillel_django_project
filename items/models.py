from pyexpat import model
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    price = models.PositiveIntegerField()
    scu = models.CharField(max_length=32)


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
