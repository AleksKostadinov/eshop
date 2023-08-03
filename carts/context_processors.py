from .models import CartItem, Cart

def counter(request):
    cart_count = 0

    if request.user.is_authenticated:
        # For authenticated users, get the user's cart and then filter cart items based on it
        cart = Cart.objects.filter(user=request.user, purchased=False).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                cart_count += cart_item.quantity

    return dict(cart_count=cart_count)
