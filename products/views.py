from django.shortcuts import render

from products.model_forms import ProductModelForm
from products.models import Product


def products(request, *args, **kwargs):
    if request.method == 'POST':
        form = ProductModelForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ProductModelForm()
    context = {
        'items': Product.objects.all(),
        'form': form
    }
    return render(request, 'products/index.html', context=context)
