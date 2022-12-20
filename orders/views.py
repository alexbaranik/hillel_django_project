from django.shortcuts import render

from orders.models import OrderItems, Discount
from orders.form import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    user = request.user
    if request.method == 'POST':
        form = OrderCreateForm(
            user=user,
            data=request.POST
            )
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItems.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            try:
                discount = form.cleaned_data['discount']
                discount.is_active = False
                discount.save()
            except Exception:
                ...
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})

    form = OrderCreateForm(user=user)
    context = {
        'cart': cart,
        'form': form
    }
    return render(request, 'orders/create.html', context)
