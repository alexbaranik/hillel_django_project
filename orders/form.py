from django import forms

from orders.models import Order, Discount


class OrderCreateForm(forms.ModelForm):
    discount = forms.ModelChoiceField(
        queryset=Discount.objects.filter(is_active=True),
        required=False
    )

    class Meta:
        model = Order
        fields = ['user', 'discount']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user.id
