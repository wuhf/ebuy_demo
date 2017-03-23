#-*- coding:utf-8 -*-
'''
    日期：2017-03-24
    时间：01:38
    author:作死小蜜蜂
'''

from rest_framework import serializers

class UsernameCheckSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)

class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30, min_length=6)
    email = serializers.EmailField(max_length=254)
    captcha = serializers.CharField(max_length=4, min_length=4)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)

class ApplyResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    captcha = serializers.CharField(max_length=4, min_length=4)

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=1, max_length=40)
    password = serializers.CharField(min_length=6, max_length=30)
    captcha = serializers.CharField(max_length=4, min_length=4)


class EditUserProfileSerializer(serializers.Serializer):
    sign = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    phone_number = serializers.CharField(max_length=11, min_length=11,required=False, allow_blank=True, default='')

class AddAddressSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    detail_address = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    phone_number = serializers.CharField(max_length=11, min_length=11)
    province = serializers.CharField(max_length=30)
    city = serializers.CharField(max_length=30)
    region = serializers.CharField(max_length=30)

