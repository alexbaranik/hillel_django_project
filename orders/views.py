from django.shortcuts import render

from orders.models import OrderItems
from orders.form import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItems.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})

    form = OrderCreateForm()
    context = {
        'cart': cart,
        'form': form
    }
    return render(request, 'orders/create.html', context)
