from email.policy import default
from operator import mod
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse


# Database schemas.
# note all id is created as pk

class Roles(models.Model):
    permissions = models.CharField(max_length=20)
    role_desc = models.CharField(max_length=20)


class Users(models.Model):
    role_id = models.ForeignKey(
        "Roles", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=1000, unique=True)
    address = models.CharField(max_length=1000, null=True, default=None)
    phone = models.CharField(max_length=15, null=True, default=None)
    allergies = models.CharField(max_length=1000, null=True)
    email_valid = models.BooleanField(default=False) #Added this cause tablebase got new column too, 1 Nov 22, 7:03PM (fumin)
    attempt = models.IntegerField(default=0)


class Product_Category(models.Model):
    category_name = models.CharField(max_length=20)


class Product_Details(models.Model):
    category_id = models.ForeignKey(
        "Product_Category", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='static/img/',null=True,blank=True)
    ingredients = models.CharField(max_length=1000)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    stock_available = models.IntegerField(null=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_details", kwargs={"slug": self.slug})


class Promotion(models.Model):
    product_id = models.ForeignKey(
        "Product_Details", on_delete=models.CASCADE)
    promotion_amount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)


class Cart(models.Model):
    product_id = models.ForeignKey(
        "Product_Details", on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        "Users", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    total_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def name(self):
        return self.product_id.name

    def pr_id(self):
        return self.product_id

    def stockavil(self):
        return self.product_id.stock_available

    def get_total_item_price(self):
        return self.quantity * self.total_price

    def get_total(self):
        total = 0
        cart = Cart.objects.all()
        total = sum(self.get_total_item_price for self in cart)
        return total


class Orders(models.Model):
    payment_mode = models.CharField(max_length=150, null=True)
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=1000, null=True)
    address = models.CharField(max_length=1000, null=True)
    phone = models.CharField(max_length=8, null=True)
    total_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    order_status = models.CharField(max_length=50, default="Pending")
    tracking_no = models.CharField(max_length=50, null=True)
    ccard_digits = models.CharField(max_length=16, blank=True, null=True)
    orderDate = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE)
    productID = models.ForeignKey(
        Product_Details, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.FloatField(null=False)

    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)


class Authorised_User(models.Model):
    role_id = models.ForeignKey(
        "Roles", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=1000)


class Product_Request(models.Model):
    user_pk_id_id = models.ForeignKey(
        "Users", on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        "Authorised_User", on_delete=models.CASCADE)
    product_id = models.ForeignKey(
        "Product_Details", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, null=True)
    created = models.CharField(max_length=50, null=True)
    updated = models.CharField(max_length=50, null=True)