from decimal import Decimal, ROUND_HALF_UP

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from cart.cart import Cart
from main.models import Size, Color, PromoCode
from orders.forms import OrderCreateForm
from orders.models import OrderItem


def order_create(request):
    cart = Cart(request)
    promo = None
    promo_slug = request.session.get('promo_code', '')

    if promo_slug:
        promo = PromoCode.objects.filter(name__iexact=promo_slug).first()
    subtotal = cart.get_total()
    total = cart.get_total(promo=promo)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in cart:
                size_id = item['size_id']
                color_id = item['color_id']
                size = get_object_or_404(Size, id=size_id)
                color = get_object_or_404(Color, id=color_id)
                price = item['price']
                if promo:
                    discount_amount = item['price'] * Decimal(promo.discount) / Decimal("100")
                    price = (item['price'] - discount_amount).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)

                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=price,
                    quantity=item['quantity'],
                    size=size,
                    color=color,
                    size_name=item['size_name'],
                    color_name=item['color_name'],
                    variant=item['product_variant']
                )
            cart.clear_items()
            request.session['order_id'] = order.id
            return redirect('main:catalog')

    else:
        form = OrderCreateForm(request=request)
    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form,  'promo': promo,'subtotal': subtotal, 'total': total,})
