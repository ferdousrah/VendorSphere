from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

# image resize livrary

from PIL import Image as PilImage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys



STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)


STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)


RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# Create your models here.

####################### Site Settings, Slider, Banners ######################



class Slider(models.Model):
    sid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="sl", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Slide Title")
    image = models.ImageField(upload_to="slides", default="slide.jpg")

    class Meta:
        verbose_name_plural = "Slider"

    def slide_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    

class HomeBanner(models.Model):
    bid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="b", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Banner Title")
    displayCode = models.CharField(max_length=10, default="B001")
    image = models.ImageField(upload_to="banners", default="banner.jpg")

    class Meta:
        verbose_name_plural = "Home Banner"

    def banner_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title    



####################### Product Settings ####################################

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Food")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    

class Tags(models.Model):
    pass
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Nestify")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    description = models.TextField(null=True, blank=True, default="I am an amazing vendor")

    address = models.CharField(max_length=100, default="123 Main Street.")
    contact = models.CharField(max_length=100, default="+8801000000000")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title


# Product Attribute and Variation models
    
class ProductAttribute(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Product Attributes"

    def __str__(self):
        return self.name

   
    
    
class ProductAttributeOption(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Product Attribute Option"
        verbose_name_plural = "Product Attribute Options"

    def __str__(self):
        return self.option
    

class ProductVariation(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='variations')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.ForeignKey(ProductAttributeOption, on_delete=models.CASCADE, verbose_name="Attribute Value")
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = "Product Variations"

    def __str__(self):
        return f"{self.product.title} - {self.attribute.name}: {self.value}"
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    
    title = models.CharField(max_length=100, default="Fresh Pear")
    imageThumb = models.ImageField(upload_to=user_directory_path, default="productThumb.jpg")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    video = models.TextField(null=True, blank=True, default="This is the product video link")
    description = models.TextField(null=True, blank=True, default="This is the product")

    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")

    specification = models.TextField(null=True, blank=True)
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    fridaySpecial = models.BooleanField(default=False)
    superDeals = models.BooleanField(default=False)
    newArrivals = models.BooleanField(default=True)
    topSeller = models.BooleanField(default=False)
    hotCategory = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        if self.old_price != 0:
            percentage = ((self.old_price - self.price) / self.old_price) * 100
            return round(percentage, 2)
        else:
            return 0
    

class ProductImages(models.Model):
    image = models.ImageField(upload_to="product-images", default="product.jpg")
    thumbnail = models.ImageField(upload_to="product-thumbnails", default="product_thumb.jpg")
    product = models.ForeignKey(Product, related_name="p_image", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Images"

    
    def save(self, *args, **kwargs):
        # Opening the uploaded image
        img = PilImage.open(self.image)

        # Resizing the image
        output_size = (300, 300)
        img.thumbnail(output_size)

        # Convert image to BytesIO object
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')

        # Set thumbnail field value
        self.thumbnail.save(self.image.name, InMemoryUploadedFile(
            thumb_io,
            None,  # None is the field name
            self.image.name,  # Name of the image
            'image/jpeg',  # MIME type
            sys.getsizeof(thumb_io),
            None
        ), save=False)

        super().save(*args, **kwargs)




################################################## Cart, Order, OrderItems and Address ######################################



class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

    class Meta:
        verbose_name_plural = "Cart Order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"
    

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    


################################################## Product Review, Wishlists, Address ######################################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"
    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"
    
    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"
