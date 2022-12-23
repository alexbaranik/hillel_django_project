from django import forms

from products.models import Product, Category
from shop.model_choices import Currency


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category')
