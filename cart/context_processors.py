from .models import Cart, CartItem
from .views import get_or_set_session_id


def cart_count(request):
    cart_count = 0
    if 'admin' in request.path:  # If there is admin word in url pattern like: http: // 127.0.0.1: 8000/admin/
        return {}   # no need to count the cart if we're in the admin section
    else:
        try:
            cart = Cart.objects.filter(
                cart_id=get_or_set_session_id(request))  # get the cart
            # if user is logged in then cart_items will be if block else it will be else block
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(
                    user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(
                    cart=cart[:1])   # get the first item in the cart
            for cart_item in cart_items:    # count the number of items in the cart
                cart_count += cart_item.quantity    # add the quantity of each item in the cart
        except Cart.DoesNotExist:   # if the cart doesn't exist
            cart_count = 0  # set the cart count to 0
    return {'cart_count': cart_count}
