from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Product, Review, Category
from .forms import UserSignupForm, UserLoginForm, ProductForm, ReviewForm

# ---------------------------
# Home & Pages
# ---------------------------
def index(request):
    products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()[:6]
    return render(request, 'home/index.html', {
        'products': products,
        'categories': categories
    })

def modal(request):
    return render(request, 'home/modal.html')

def notification_toast(request):
    return render(request, 'home/notification-toast.html')

def product(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'home/product.html', {'products': products})

def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    
    # Check if user has already reviewed this product
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
    
    reviews = Review.objects.filter(product=product).order_by('-review_date')
    review_form = ReviewForm(instance=user_review) if user_review else ReviewForm()
    
    return render(request, 'home/product_details.html', {
        'product': product,
        'review_form': review_form,
        'reviews': reviews,
        'user_review': user_review
    })

def category(request):
    categories = Category.objects.all()
    return render(request, 'home/category.html', {'categories': categories})

def product_box(request):
    products = Product.objects.filter(is_active=True)[:4]
    return render(request, 'home/product_box.html', {'products': products})

def product_feature(request):
    products = Product.objects.filter(is_active=True)[:3]
    return render(request, 'home/product_feature.html', {'products': products})

def product_grid(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'home/product_grid.html', {'products': products})


# ---------------------------
# Authentication
# ---------------------------
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Account created successfully!')
            
            if user.role == 'seller':
                return redirect('seller_dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserSignupForm()
    
    return render(request, 'authentication/signup.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            if user.role == 'seller':
                return redirect('seller_dashboard')
            elif user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

def forget(request):
    return render(request, 'authentication/forget.html')

def logout(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


# ---------------------------
# Seller Dashboard & Products
# ---------------------------
@login_required
def seller_dashboard(request):
    if request.user.role != 'seller':
        messages.error(request, 'Access denied. Seller account required.')
        return redirect('index')
    
    products = Product.objects.filter(seller=request.user)
    return render(request, 'seller/dashboard.html', {'products': products})

@login_required
def product_add(request):
    if request.user.role != 'seller':
        messages.error(request, 'Access denied. Seller account required.')
        return redirect('index')
    
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('seller_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    
    return render(request, 'seller/product_form.html', {'form': form, 'action': 'Add'})

@login_required
def product_edit(request, pk):
    if request.user.role != 'seller':
        messages.error(request, 'Access denied. Seller account required.')
        return redirect('index')
    
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('seller_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'seller/product_form.html', {'form': form, 'action': 'Edit', 'product': product})

@login_required
def product_delete(request, pk):
    if request.user.role != 'seller':
        messages.error(request, 'Access denied. Seller account required.')
        return redirect('index')
    
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    
    if request.method == "POST":
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('seller_dashboard')
    
    return render(request, 'seller/product_confirm_delete.html', {'product': product})


# ---------------------------
# Add Review (Buyer)
# ---------------------------
@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    
    # Check if user already reviewed this product
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.warning(request, 'You have already reviewed this product.')
        return redirect('product_details', pk=pk)
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Your review has been added!')
        else:
            messages.error(request, 'Please correct the errors in your review.')
    
    return redirect('product_details', pk=pk)


# User Dashboard Home
@login_required
def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

# Profile View & Update
@login_required
def user_profile(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # Update profile info
        request.user.first_name = name
        request.user.email = email
        request.user.profile.phone = phone
        request.user.profile.address = address
        request.user.save()
        request.user.profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("user_profile")

    return render(request, "profile/user.html")

# User Orders
@login_required
def user_orders(request):
    orders = request.user.order_set.all()  # ধরলাম order model এ user ForeignKey আছে
    return render(request, "dashboard/user_orders.html", {"orders": orders})

# Wishlist
@login_required
def user_wishlist(request):
    wishlist = request.user.wishlist_set.all()  # ধরলাম wishlist model এ user ForeignKey আছে
    return render(request, "dashboard/user_wishlist.html", {"wishlist": wishlist})

# Cart
@login_required
def user_cart(request):
    cart_items = request.user.cartitem_set.all()  # ধরলাম cart model এ user ForeignKey আছে
    return render(request, "dashboard/user_cart.html", {"cart_items": cart_items})

# Settings (Change Password Page)
@login_required
def user_settings(request):
    return render(request, "dashboard/user_settings.html")