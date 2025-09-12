from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'home/index.html')

def modal(request):
    return render(request, 'home/modal.html')

def notification_toast(request):
    return render(request, 'home/notification-toast.html')

def product(request):
    return render(request, 'home/product.html')

def product_details(request):
    return render(request, 'home/product_details.html')

def category(request):
    return render(request, 'home/category.html')

def product_box(request):
    return render(request, 'home/product_box.html')

def product_feature(request):
    return render(request, 'home/product_feature.html')

def product_grid(request):
    return render(request, 'home/product_grid.html')

def signup(request):
    return render(request, 'authentication/signup.html')

def forget(request):
    return render(request, 'authentication/forget.html')

def login(request):
    return render(request, 'authentication/login.html')
