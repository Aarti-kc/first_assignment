"""auctions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from auction_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('logout_user', views.ProductSection.logout_user, name='logout_user'),
    path('', views.index, name='index'),
    path('add_product', views.ProductSection.add_product, name='Add New Product'),
    path('add_product_save', views.ProductSection.add_product_save, name='Save Product'),
    path('details/<int:id>', views.ProductSection.details, name='More Details'),
    path('bidding/<int:pro_id>', views.ProductSection.bidding, name='Update price'),
    path('add_product_bidding_save', views.ProductSection.add_product_bidding_save, name='add_product_bidding_save'),

   
    path('login', views.ProductSection.login_now, name="login"),
    path('login_user', views.ProductSection.login_user, name="login User"),
    
    path('register_user', views.ProductSection.register_user, name='register_user'),
    path('register_user_save', views.ProductSection.register_user_save, name='register_user_save'),
    path('watchlist_add/<int:product_id>', views.ProductSection.watchlist_add, name="User WatchList"),
    path('all_watchlist', views.ProductSection.all_watchlist, name="All WatchList items"),
    path('remove_from_watchlist/<int:pro_id>', views.ProductSection.remove_from_watchlist, name="Remove from WatchList"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)