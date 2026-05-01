from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddForm
from main.models import Product, PromoCode


# Create your views here.

def get_cart_context(request, message=''):
    cart = Cart(request)
    promo_slug = request.session.get('promo_code', '')
    promo = None
    if promo_slug:
        promo = PromoCode.objects.filter(name__iexact=promo_slug).first()
    return {
        'cart': cart,
        'subtotal': cart.get_total(),
        'total': cart.get_total(promo=promo),
        'promo': promo,
        'message': message,
    }


def detail(request):
    return render(request, 'cart/cart_detail.html', get_cart_context(request))


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
        return render(request, 'cart/partials/cart_response.html', get_cart_context(request))
    return redirect('cart:detail')


def clear(request):
    cart = Cart(request)
    cart.clear_items()
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'cart/partials/cart_response.html', get_cart_context(request))
    return redirect('cart:detail')



def update_quantity(request, cart_key):
    cart = Cart(request)
    action = request.GET.get('action', '')

    cart.update_quantity(cart_key=cart_key, action=action)
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'cart/partials/cart_response.html', get_cart_context(request))
    return redirect('cart:detail')


def promo_apply(request):
    promo_slug = request.GET.get('promo', '').strip()
    promo = PromoCode.objects.filter(name__iexact=promo_slug).first()

    if promo:
        request.session["promo_code"] = promo.name
        message = "Promo code applied"
    else:
        request.session.pop("promo_code", None)
        message = "Invalid promo code"


    if request.headers.get('HX-Request') == 'true':
        return render(request, 'cart/partials/cart_partial.html', get_cart_context(request, message))
    return redirect('cart:detail')

def promo_remove(request):
    request.session.pop('promo_code', None)
    request.session.modified = True
    message = ""


    if request.headers.get('HX-Request') == 'true':
        return render(request, 'cart/partials/cart_partial.html', get_cart_context(request, message))
    return redirect('cart:detail')


