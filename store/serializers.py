#-*- coding:utf-8 -*-
'''
    日期：2017-03-24
    时间：22:44
    author:作死小蜜蜂
'''

from rest_framework import serializers

class AddItemtoCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class CartItemOpSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    is_add = serializers.BooleanField()

class DeleteCartItemSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()