from shop_app.models import Product

def users_wishlist(request):
    if request.user.is_authenticated:
        users_wishlist = Product.objects.filter(users_wishlist=request.user)
    else:
        users_wishlist = []

    return {
        'users_wishlist': users_wishlist,
    }
