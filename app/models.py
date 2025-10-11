from django.db import models
from django.db.models import AutoField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


class Customer (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)          # Full name
    phone_no = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('M', 'Men'),
    ('W', 'Women'),
    ('J', 'Jewelry'),
    ('O','Medicine'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField(default='null')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    p_image = models.ImageField(upload_to='product_img')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products',null=True, blank=True) # Added owner field
    quantity = models.PositiveIntegerField(default=0)  # 🧮 নতুন field

    def __str__(self):
        return str(self.title)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)
SIZE_CHOICES = (
    ('X', 'small'),
    ('M', 'medium'),
    ('L', 'large'),
    ('XL', 'extra large'),
)


class OrderPlaced (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(choices=SIZE_CHOICES, max_length=2, default='M')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class ChatHistory(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    user = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.content}'