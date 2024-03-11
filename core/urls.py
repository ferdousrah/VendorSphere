from django.urls import path
from core.views import category_list_view, category_product_list_view, product_detail_view, index, add_to_cart, cart_view

app_name = "core"

urlpatterns = [
    path("", index, name="index"),

    # Ctaegory
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),

    # Product
    path("product/<pid>/", product_detail_view, name="product-detail"),

    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    path("cart/", cart_view, name="cart"),

]