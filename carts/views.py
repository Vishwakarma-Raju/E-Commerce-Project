from django.shortcuts import render , redirect
from store.models import Product
from .models import Cart , CartItem

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        return cart

def add_cart(request, product_id):
    product = Product.object.get(id=product_id) # get the product

    try:
        cart = Cart.object.get(cart_id=_cart_id) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.object.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.object.get(product=product , cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.object.create(
            product = product,
            cart = cart,
            quantity = 1,
        )
        cart_item.save()
    return redirect('cart')


def cart(request):
    return render(request, 'store/cart.html')