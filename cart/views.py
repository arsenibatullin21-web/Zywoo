from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddForm
from main.models import Product


# Create your views here.

def detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@require_POST
def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            color=cd['color'],
            size=cd['size']
        )

    if request.headers.get('HX-Request') == 'true':
        return render(request, 'cart/partials/cart-budge.html')
    return redirect(product.get_absolute_url())

@require_POST
def remove(request, cart_key):
    cart = Cart(request)
    cart.remove(cart_key)
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'cart/partials/cart_response.html')
    return redirect('cart:detail')


def clear(request):
    cart = Cart(request)
    cart.clear_items()
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'cart/partials/cart_response.html')
    return redirect('cart:detail')



def update_quantity(request, cart_key):
    cart = Cart(request)
    action = request.GET.get('action', '')

    cart.update_quantity(cart_key=cart_key, action=action)
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'cart/partials/cart_response.html')
    return redirect('cart:detail')
