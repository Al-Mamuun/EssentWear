from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.Productview.as_view(), name="home"),
    path('product-detail/<int:pk>', views.ProductDeatilView.as_view(), name='product-detail'),
     path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete'),
     path('product/<int:pk>/edit/', views.product_edit, name='product-edit'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart,),
    path('minuscart/', views.minus_cart,),
    path('removecart/', views.remove_cart,),

    path('contact-us/', views.contactus, name='contact-us'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),

    path('men/', views.football, name='men'),
    #path('football/<slug:data>', views.football, name='footballdata'),
    path('women/', views.cricket, name='women'),
    path('jwellery/', views.jwellery, name='jwellery'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),


    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = 'app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-Complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/logout.html'), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    path('checkout/', views.checkout, name='checkout'),
    path('orderdone/', views.order_done, name='orderdone'),
    path('orders/', views.orders, name='orders'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('search/', views.search_products, name='search_products'),

    path('mamun/', views.mamun, name='mamun'),
    
    path('faq/', views.faq, name='faq'),
    path('return-policy/', views.return_policy, name='return_policy'),
    path('size-guide/', views.size_guide, name='size_guide'),
    path('shipping-info/', views.shipping_info, name='shipping_info'),
    
    path('add-product/', views.add_product, name='add_product')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
