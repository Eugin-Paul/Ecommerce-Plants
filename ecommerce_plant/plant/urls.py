from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('cart', views.cart, name = 'cart'),
    path('address', views.address, name = 'address'),
    path('plants/<product_id>', views.plants, name = 'plants'),
    path('register', views.register, name = 'register'),
    path('login', views.loginpage, name = 'loginpage'),
    path('logout', views.logoutpage, name = 'logoutpage'),
    path('search', views.search, name = 'search'),
    path('pincode/<product_id>', views.pincode, name = 'pincode'),
    path('sort_low_to_high', views.sort_low_to_high, name = 'sort_low_to_high'),
    path('sort_high_to_low', views.sort_high_to_low, name = 'sort_high_to_low'),
    path('sort_new', views.sort_new, name = 'sort_new'),
    path('sort_old', views.sort_old, name = 'sort_old'),
    path('updateitem', views.updateitem, name = 'updateitem'),
]
