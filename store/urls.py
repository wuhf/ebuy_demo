"""ebuy_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', view=views.index),
    url(r'^index/$', view=views.index, name='index'),
    url(r'^pruduct/(?P<id>\d+)', view=views.product, name='product'),
    url(r'^category/(?P<id>\d+)', view=views.categpries, name='category'),
    url(r'^search/$', view=views.search, name='search'),
    url(r'^view_cart/$', views.view_cart, name='view_cart'),
    url(r'^add_to_cart/$', views.AddProductToCartView.as_view(), name='add_to_cart'),
    url(r'^cartnum_op/$', views.CartItemOpView.as_view(), name='cartnum_op'),
    url(r'^delete_cart_item/$', views.DeleteCartItemView.as_view(), name='delete_cart_item'),
    url(r'^clear_cart/$', views.CartClearView.as_view(), name='clear_cart'),
]
