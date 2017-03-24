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
from . import views

urlpatterns = [
    url(r'^register/$', views.UserRegisterView.as_view(), name='register'),
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^captcha/$', views.show_captcha, name="show_captcha"),
    url(r'^username_check/$', views.account_username_check, name='username_check'),
    url(r'^email_check/$', views.api_email_check, name='email_check'),
    url(r'^reset_password/$', views.UserResetPwdView.as_view(), name='apply_reset_password'),
    url(r'^reset_email_check/$', views.api_reset_email_check, name='reset_email_check'),
    url(r'^apply_reset_password/(?P<token>\w+)/$', views.apply_reset_password, name="apply_reset_password"),
    url(r'^apply_reset_password/$', views.reset_password, name="apply_reset_password"),
    url(r'^account/user/(?P<username>\w+)/$', views.user_info, name="user_info"),
    url(r'^account/settings/$', views.UserSettingView.as_view(), name="user_setting"),
    url(r'^account/settings/avatar/$', views.UserAvatarView.as_view(), name="user_avatar"),
    url(r'^account/settings/address/$', views.UserAddressView.as_view(), name="user_address"),
]
