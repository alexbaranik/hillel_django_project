from django.shortcuts import get_object_or_404, render, redirect

from orders.models import OrderItems, Order
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


def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_paid = True
    order.total_amount = order.get_total_amount()
    order.save(update_fields=('total_amount', 'is_paid',))
    return redirect('products')
