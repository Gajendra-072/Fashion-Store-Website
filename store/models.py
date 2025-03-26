from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length=100, default="Default Brand")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('U', 'Unisex'),
    ]

    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', '2X Large'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=255, default="Default Brand")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    additional_images = models.ManyToManyField('ProductImage', blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    sizes = models.ManyToManyField('Size')
    colors = models.ManyToManyField('Color')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        if self.sale_price:
            return int(((self.price - self.sale_price) / self.price) * 100)
        return 0

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image {self.id}"

class Size(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7)  # Hex color code

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def subtotal(self):
        if self.product.sale_price:
            return self.product.sale_price * self.quantity
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    payment_status = models.CharField(max_length=20, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def subtotal(self):
        return self.price * self.quantity
