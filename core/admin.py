from django.contrib import admin
from django import forms
from core.models import Product, ProductAttribute, ProductVariation, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address, Slider, HomeBanner, ProductAttributeOption

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductVariationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductVariationForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['value'].queryset = ProductAttributeOption.objects.filter(attribute=self.instance.attribute)
        else:
            self.fields['value'].queryset = ProductAttributeOption.objects.none()

    class Meta:
        model = ProductVariation
        fields = '__all__'

class ProductAttributeOptionInline(admin.TabularInline):
    model = ProductAttributeOption
    extra = 1  # Number of empty forms to display

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    form = ProductVariationForm
    extra = 1


class ProductAttributeAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeOptionInline]
    list_display = ['name', 'description']

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, ProductVariationInline]
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'vendor', 'featured', 'product_status', 'pid']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'slide_image']

class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'displayCode', 'banner_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']

# Register your models here.
    
# Ensure the ProductAttribute is registered using the new admin class
admin.site.register(ProductAttribute, ProductAttributeAdmin)

admin.site.register(Product, ProductAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Slider, SliderAdmin)

admin.site.register(HomeBanner, HomeBannerAdmin)

admin.site.register(Vendor, VendorAdmin)

admin.site.register(CartOrder, CartOrderAdmin)

admin.site.register(CartOrderItems, CartOrderItemsAdmin)

admin.site.register(ProductReview, ProductReviewAdmin)

admin.site.register(Wishlist, WishlistAdmin)

admin.site.register(Address, AddressAdmin)
