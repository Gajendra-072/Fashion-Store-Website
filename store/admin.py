from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, Size, Color, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'description')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock', 'gender')
    list_filter = ('category', 'brand', 'gender')
    search_fields = ('name', 'description')
    filter_horizontal = ('sizes', 'colors', 'additional_images')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_filter = ('user',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'size', 'color')
    list_filter = ('cart', 'product', 'size', 'color')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'payment_status')
    list_filter = ('status', 'payment_status')
    search_fields = ('user__username', 'shipping_address')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'size', 'color')
    list_filter = ('order', 'product', 'size', 'color')
