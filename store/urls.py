from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # This is the OLD path. DELETE this line:
    # path('register/', views.register, name='register'), 
    
    # This is the NEW path. Keep this one:
    path('register/', TemplateView.as_view(template_name='store/register.html'), name='register'),
    
    # This path is for the NEW Firebase login:
    path('login/', TemplateView.as_view(template_name='store/login.html'), name='login'),

    # This path is for the Django logout, which we still need:
    path('logout/', views.custom_logout, name='logout'),
    
    path('', views.home, name='home'),
    path('account/', views.my_account, name='my_account'),
    path('sell/', views.create_product, name='create_product'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('category/<int:category_id>/', views.category_page, name='category_page'),
    path('firebase-login/', views.firebase_login, name='firebase_login'),
]