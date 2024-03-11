from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address, Slider, HomeBanner


def default(request):
    categories = Category.objects.all().order_by("-id")

    return{
        'categories': categories,
    }


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty'])*float(item['price'])
        return {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), "cart_total_amount": cart_total_amount}
    else:
        return {"cart_data":'', 'totalcartitems': 0, "cart_total_amount": cart_total_amount}