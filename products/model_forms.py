from django import forms

from products.models import Product, Category
from shop.model_choices import Currency


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category')


class ProductFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        empty_label="Select"
    )
    currency = forms.ChoiceField(
        required=False,
        choices=[('', 'Select')] + Currency.choices,
    )
    name = forms.CharField(max_length=255, required=False)
