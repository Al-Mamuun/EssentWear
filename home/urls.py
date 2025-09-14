from django.urls import path
from . import views

urlpatterns = [
    # Home & Common Pages
    path('', views.index, name='index'),
    path('modal/', views.modal, name='modal'),
    path('notification-toast/', views.notification_toast, name='notification_toast'),
    path('products/', views.product, name='product'),
    path('product/<int:pk>/', views.product_details, name='product_details'),
    path('category/', views.category, name='category'),
    path('product-box/', views.product_box, name='product_box'),
    path('product-feature/', views.product_feature, name='product_feature'),
    path('product-grid/', views.product_grid, name='product_grid'),

    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('forget-password/', views.forget, name='forget'),
    path('logout/', views.logout, name='logout'),

    # Seller Dashboard & Products
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/product/add/', views.product_add, name='product_add'),
    path('seller/product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('seller/product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # User Profile
    path('profile/', views.user_profile, name='user_profile'),

    # Buyer Reviews
    path('product/<int:pk>/review/', views.add_review, name='add_review'),
    
]
