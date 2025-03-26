from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from decimal import Decimal
from .utils import get_fashion_image, get_category_images, get_single_image

def home(request):
    # Get featured products (using first 4 products as featured)
    featured_products = Product.objects.all()[:4]
    
    # Get all products for the men's section
    all_products = Product.objects.all()[:6]
    
    # Get category images
    hero_image = get_fashion_image('fashion-store-hero')
    category_images = [
        get_fashion_image('men-clothing'),
        get_fashion_image('women-clothing'),
        get_fashion_image('men-shoes'),
        get_fashion_image('women-shoes')
    ]
    men_images = [
        get_fashion_image('men-clothing-1'),
        get_fashion_image('men-clothing-2'),
        get_fashion_image('men-clothing-3')
    ]
    
    # Get cart count for authenticated users
    cart_count = None
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(cart__user=request.user).count()
    
    context = {
        'featured_products': featured_products,
        'all_products': all_products,
        'hero_image': hero_image,
        'category_images': category_images,
        'men_images': men_images,
        'cart_count': cart_count,
    }
    return render(request, 'store/home.html', context)

def product_list(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    
    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)
    
    # Get featured product images
    featured_images = get_category_images('men-clothing', count=3)
    
    context = {
        'products': products,
        'featured_images': featured_images,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Get related product images
    related_images = get_category_images(product.category.slug, count=3)
    
    context = {
        'product': product,
        'related_images': related_images,
    }
    return render(request, 'store/product_detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    
    # Get category images
    category_images = get_category_images(slug, count=4)
    
    context = {
        'category': category,
        'products': products,
        'category_images': category_images,
    }
    return render(request, 'store/category_detail.html', context)

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    
    # Calculate totals
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    tax = subtotal * 0.1  # 10% tax
    total = subtotal + tax
    
    # Get featured images for fallback
    featured_images = get_category_images('men-clothing', count=3)
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        'featured_images': featured_images,
    }
    return render(request, 'store/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('store:cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('store:cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    
    return redirect('store:cart')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Process the order
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            total_amount=cart.total,
            status='pending'
        )
        # Clear the cart
        cart.items.all().delete()
        return redirect('store:cart')
    
    return render(request, 'checkout.html', {'cart': cart})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('store:login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    context = {
        'orders': orders,
    }
    return render(request, 'store/profile.html', context)
