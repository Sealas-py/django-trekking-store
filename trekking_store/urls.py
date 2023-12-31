"""
URL configuration for trekking_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from store.views import CategoryDetailView, IndexView, ProductDetailView, CartView, OrderView, UserProfileView, \
    UserOrdersView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('accounts/', include('allauth.urls')),
    path('category/<slug:slug>', CategoryDetailView.as_view(), name='category'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product'),
    path('cart', CartView.as_view(), name='cart'),
    path('order', OrderView.as_view(), name='place_order'),
    path('profile', UserProfileView.as_view(), name='user_profile'),
    path('profile/orders', UserOrdersView.as_view(), name='user_orders'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
