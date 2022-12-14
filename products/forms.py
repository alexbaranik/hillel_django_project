from django import forms

from products.models import Category, Item


class ItemForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    image = forms.ImageField()
    category = forms.CharField()

    def is_valid(self):
        """
        Validate data
        :return:
        """
        is_valid = super().is_valid()
        if is_valid:
            category_name = self.cleaned_data['category']
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                self.errors.update(
                    {'category': f'Category {category_name} does not exist.'}
                )
            else:
                self.cleaned_data['category'] = category
        return is_valid

    def save(self):
        """
        Create Item instance in database
        :return:
        """
        return Item.objects.create(**self.cleaned_data)
