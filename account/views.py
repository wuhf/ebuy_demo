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
from django.utils import timezone
import codecs
from django.conf import settings
from utils.email import send_email


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


class UserResetPwdView(APIView):
    def get(self, request):
        return render_to_response('account/reset_password.html')

    def post(self, request):
        serializer = ApplyResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            captcha = Captcha(request)
            if not captcha.check(data["captcha"]):
                return error_response(u"验证码错误")
            try:
                user = User.objects.get(email=data["email"])
            except User.DoesNotExist:
                return error_response(u"用户不存在")
            rand_str_ = rand_str()
            user.reset_password_token = rand_str_
            user.reset_password_token_create_time = timezone.now()
            user.save()
            email_template = codecs.open(settings.TEMPLATES[0]["DIRS"][0] + "/account/reset_password_email.html", "r",
                                         "utf-8").read()

            email_template = email_template.replace("{{ username }}", user.username). \
                replace("{{ website_name }}", settings.WEBSITE_INFO["website_name"]). \
                replace("{{ link }}", settings.WEBSITE_INFO["url"] + "/apply_reset_password/" +
                        user.reset_password_token)

            send_email(settings.WEBSITE_INFO["website_name"],
                              user.email,
                              user.username,
                              settings.WEBSITE_INFO["website_name"] + u" 登录信息找回邮件",
                              email_template)
            return success_response(u"邮件发送成功,请前往您的邮箱查收")
        else:
            return serializer_invalid_response(serializer)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def show_captcha(request):
   return Captcha(request).display()

def error_page(request, error_reason):
    return render(request, "error.html", {"error": error_reason})

def apply_reset_password(request, token):
    try:
        user = User.objects.get(reset_password_token=token)
    except User.DoesNotExist:
        return error_page(request, u"链接已失效")
    if (timezone.now() - user.reset_password_token_create_time).total_seconds() > 30 * 60:
        return error_page(request, u"链接已过期")
    return render(request, "account/apply_reset_pwd.html", {"user": user})

@api_view(['POST',])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.data
        captcha = Captcha(request)
        if not captcha.check(data["captcha"]):
            return error_response(u"验证码错误")
        try:
            user = User.objects.get(reset_password_token=data["token"])
        except User.DoesNotExist:
            return error_response(u"token 不存在")
        if (timezone.now() - user.reset_password_token_create_time).total_seconds() > 30 * 60:
            return error_response(u"token 已经过期，请在30分钟内重置密码")
        user.reset_password_token = None
        user.set_password(data["password"])
        user.save()
        return success_response(u"密码重置成功")
    else:
        return serializer_invalid_response(serializer)