from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('modal/', views.modal, name='modal'),
    path('notification-toast/', views.notification_toast, name='notification_toast'),
    path('product/', views.product, name='product'),
    path('product-details/', views.product_details, name='product_details'),
    path('category/', views.category, name='category'),
    path('product-box/', views.product_box, name='product_box'),
    path('signup/', views.signup, name='signup'),
    path('forget/', views.forget, name='forget'),
    path('login/', views.login, name='login'),
]
