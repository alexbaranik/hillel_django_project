import csv
import decimal

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import OuterRef, Exists
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView

from weasyprint import HTML

from products.model_forms import ProductFilterForm, ProductModelForm
from products.models import Product, Category
from cart.forms import CartAddProductForm


# def products(request, *args, **kwargs):
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#     else:
#         form = ProductModelForm()
#     context = {
#         'items': Product.objects.all(),
#         'form': form
#     }
#     return render(request, 'products/index.html', context=context)


def products(request, *args, **kwargs):
    page_number = request.GET.get('page')
    paginator = Paginator(Product.objects.all(), 10)
    pages = paginator.get_page(page_number)
    cart_product_form = CartAddProductForm()
    context = {
        'object_list': pages,
        'cart_product_form': cart_product_form,
    }
    return render(request, context=context,
                  template_name='products/product_list.html')


class ProductsView(ListView):
    model = Product
    paginate_by = 10
    filter_form = ProductFilterForm

    def filtered_queryset(self, queryset):
        category_id = self.request.GET.get('category')
        currency = self.request.GET.get('currency')
        name = self.request.GET.get('name')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if currency:
            queryset = queryset.filter(currency=currency)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_queryset(self):
        qs = self.model.get_products().prefetch_related('favorites')
        qs = self.filtered_queryset(qs)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        user_favorites = Product.objects.filter(favorites=self.request.user)
        context.update({
            'cart_product_form': cart_product_form,
            'user': self.request.user,
            'filter_form': self.filter_form,
            'user_favorites': user_favorites
        })
        return context


class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context.update({'cart_product_form': cart_product_form})
        return context


@login_required
def export_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="products.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(
        ['name', 'description', 'category', 'price', 'sku', 'image']
    )
    for product in Product.objects.iterator():
        writer.writerow(
            [
             product.name,
             product.description,
             product.price,
             product.sku,
             product.category,
             settings.DOMAIN + product.image.url
            ]
        )
    return response


@login_required
def import_csv(request):
    products_list = []
    with open('import_products.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for product in reader:
            products_list.append(
                Product(
                    name=product['name'],
                    description=product['description'],
                    price=decimal.Decimal(product['price']),
                    sku=product['sku'],
                    category=Category.objects.get_or_create(
                        name=product['category']
                    )[0]
                )
            )
        Product.objects.bulk_create(products_list)
    return HttpResponse('Import success!')


class ExportPDF(TemplateView):
    template_name = 'products/pdf.html'

    def get(self, request, *args, **kwargs):
        html = loader.render_to_string(
            template_name=self.template_name,
            context=self.get_context_data()
        )
        pdf = HTML(string=html).write_pdf()
        response = HttpResponse(
            pdf,
            content_type='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename="products.pdf"'
            }
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'products': Product.objects.all(),
                        'domain': settings.DOMAIN})
        return context


@login_required
def favorites(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    if product.favorites.filter(id=user.id).exists():
        product.favorites.remove(user)
    else:
        product.favorites.add(user)
    return HttpResponseRedirect(reverse_lazy('products'))


@login_required
def product_favorite_list(request):
    user = request.user
    favorite_products = user.favorites.all()
    cart_product_form = CartAddProductForm()
    context = {
        'favorite_products': favorite_products,
        'cart_product_form': cart_product_form
    }
    return render(request, 'favorites/product_favorite_list.html', context)
