from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Count

from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address, Slider, HomeBanner

# Create your views here. # products = Product.objects.filter(featured=True)

    # products = Product.objects.filter(product_status='Published', featured=True)

def index(request):  
        
    products = Product.objects.all().order_by("-id")

    slides = Slider.objects.all().order_by("-id")

    categories = Category.objects.all().order_by("-id")

    miniBannerOne = HomeBanner.objects.filter(displayCode='MB1')

    miniBannerTwo = HomeBanner.objects.filter(displayCode='MB2')

    midBannerOne = HomeBanner.objects.filter(displayCode='MID1')

    midBannerTwo = HomeBanner.objects.filter(displayCode='MID2')

    midBannerThree = HomeBanner.objects.filter(displayCode='MID3')

    context = {
        "products":products,
        "slides":slides,
        "miniBannerOne": miniBannerOne,
        "miniBannerTwo": miniBannerTwo,
        "categories": categories,
        "midBannerOne": midBannerOne,
        "midBannerTwo": midBannerTwo,
        "midBannerThree": midBannerThree,
    }

    return render(request, 'core/index.html', context)


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories": categories,
    }

    return render(request, 'core/category-list.html', context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)

    context = {
        "category": category,
        "products": products,
    }

    return render(request, "core/category-product-list.html", context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    #product = get_object_or_404(Product, pid=pid)

    rproducts = Product.objects.filter(category=product.category).exclude(pid=pid)

    p_image = product.p_image.all()

    context = {
        
        "product": product,
        "p_image": p_image,
        "rproducts": rproducts,
        
    }


    return render(request, "core/product-detail.html", context)



def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})



def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty'])*float(item['price'])
        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), "cart_total_amount": cart_total_amount})
    else:
        return redirect('core:index')
    





