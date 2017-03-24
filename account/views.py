from django.shortcuts import render, render_to_response,HttpResponseRedirect,Http404
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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
                UserProfile.objects.create(user=user)
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

def user_info(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return error_page(request, u"用户不存在")

    return render(request, "account/user_index.html", {"user": user})

class UserSettingView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "account/setting.html")

    @method_decorator(login_required)
    def post(self, request):
        serializer = EditUserProfileSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user_profile = request.user.userprofile
            if data["sign"]:
                user_profile.sign = data["sign"]
                print('sign ', user_profile.sign)
            if data["phone_number"]:
                user_profile.phone_number = data["phone_number"]

            user_profile.save()
            return success_response(u"修改成功")
        else:
            return serializer_invalid_response(serializer)

class UserAvatarView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "account/setting_avatar.html")

    @method_decorator(login_required)
    def post(self, request):
        try:
            f = request.FILES["avatar"]
        except Exception:
            return Http404()

        if f.size > 1024 * 1024:
            return Http404()

        if os.path.splitext(f.name)[-1].lower() not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
            return Http404()

        user_profile = request.user.userprofile
        user_profile.avatar = f
        user_profile.save()
        return render(request, 'account/setting.html')

class UserAddressView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "account/setting_address.html")

    @method_decorator(login_required)
    def post(self, request):
        serializer = AddAddressSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            print(type(request.user),dir(request.user))
            user_profile = request.user.userprofile
            is_modify = False
            try:
                address_id = data['address_id']
                address = Address.objects.get(pk=address_id)
                is_modify = True
                address.name = data['name']
                address.phone_number = data['phone_number']
                address.province = data['province']
                address.city = data['city']
                address.region = data['region']
                address.email = data['email']
                address.detail_address = data['detail_address']
                address.save()
            except Address.DoesNotExist:
                address = Address(name=data['name']
                                  , phone_number=data['phone_number']
                                  , province=data['province']
                                  , city=data['city']
                                  , region=data['region']
                                  , email=data['email']
                                  , detail_address=data['detail_address'])
                address.save()
                user_profile.address_info.add(address)


            user_profile.save()
            return success_response({'id':address.id, 'is_modify':is_modify})
        else:
            return serializer_invalid_response(serializer)

    @method_decorator(login_required)
    def delete(self, request):
        address_id = request.data['address_id']
        try:
            address = Address.objects.get(pk=address_id)
            request.user.userprofile.address_info.remove(address)
            address.delete()
        except Address.DoesNotExist:
            return error_response('not exit')

        return success_response(address_id)
