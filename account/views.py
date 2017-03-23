from django.shortcuts import render, render_to_response,HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from utils.captcha import Captcha
from utils.utils import *
from .models import *
from django.contrib.auth import logout, login, authenticate
from django.contrib import auth


# Create your views here.
class UserRegisterView(APIView):
    def get(self, request):
        return render_to_response('account/register.html')

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.POST)
        if serializer.is_valid():
            data = serializer.data
            captcha = Captcha(request)
            if not captcha.check(data["captcha"]):
                return error_response(u"验证码错误")
            try:
                User.objects.get(username=data["username"])
                return error_response(u"用户名已存在")
            except User.DoesNotExist:
                pass
            try:
                User.objects.get(email=data["email"])
                return error_response(u"该邮箱已被注册，请换其他邮箱进行注册")
            except User.DoesNotExist:
                user = User.objects.create(username=data["username"], email=data["email"])
                user.set_password(data["password"])
                user.save()
                return success_response(u"注册成功！")
        else:
            return serializer_invalid_response(serializer)


@api_view(['GET', ])
def account_username_check(request):
    username = request.GET.get("username", None)
    if username:
        try:
            User.objects.get(username=username)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def api_email_check(request):
    email = request.GET.get("email", None)
    if email:
        try:
            User.objects.get(email=email)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def api_reset_email_check(request):
    email = request.GET.get("email", None)
    if email:
        try:
            User.objects.get(email=email)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def get(self, request):
        return render_to_response('account/login.html')

    def post(self, request):
        serializer = UserLoginSerializer(data=request.POST)
        if serializer.is_valid():
            data = serializer.data
            user = authenticate(username=data["username"], password=data["password"])
            if user:
                auth.login(request, user)
                return success_response("登录成功")
            else:
                return error_response("用户名或密码错误")
        else:
            return serializer_invalid_response(serializer)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def show_captcha(request):
   return Captcha(request).display()