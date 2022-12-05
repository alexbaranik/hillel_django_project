from django.urls import reverse

from products.models import Product


def test_order_create(login_user, client, faker, product_factory):
    product_factory()
    test_products = Product.objects.all()
    for items in test_products:
        data = {
            'quantity': faker.random_int(min=1, max=10),
        }
        response = client.post(reverse('cart_add', args=(items.id,)), data=data, follow=True)
        assert response.status_code == 200

    assert not response.context['cart'].cart.__len__() == 0
    
    data = {
        'cart': response.context['cart'].cart,
    }
    
    client, user = login_user
    
    data['form'] = {
        'user': user
    }

    response = client.get(reverse('order_create'), data=data, follow=True)
    assert response.status_code == 200
   
    response = client.post(reverse('order_create'), data=data, follow=True)
    assert response.status_code == 200
  
