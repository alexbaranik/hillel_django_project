import tempfile
from decimal import Decimal
from django.shortcuts import redirect
from django.urls import reverse
from products.models import Product, Category
from orders.models import Order, OrderItems


def test_order_create(login_user, client, faker):
    url = reverse('products')
    
    category = Category.objects.create(
        name=faker.word(),
        description=faker.text()
    )
    name = faker.word()
    description = faker.text()
    price = Decimal('20.40')
    currency = 'UAH'
    sku = '392847'
    image = tempfile.NamedTemporaryFile(suffix=".jpg").name

    product = Product.objects.create(
        name=name,
        description=description,
        image=image,
        category=category,
        price=price,
        currency=currency,
        sku=sku
    )

    assert Product.objects.exists()

    data = {
        'quantity': 5,
    }
    response = client.post(reverse('cart_add', args=(product.id,)), data=data, follow=True)
    assert response.status_code == 200
    assert not response.context['cart'].cart.__len__() == 0

    data = {
        'cart': response.context['cart'].cart,
    }

    response = client.get(reverse('order_create'), data=data, follow=True)
    assert response.status_code == 200
   
    client, user = login_user

    data['form'] = {
        'user': user
    }

    response = client.post(reverse('order_create'), data=data, follow=True)
    assert response.status_code == 200
    breakpoint()
