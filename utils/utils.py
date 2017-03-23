#-*- coding:utf-8 -*-
'''
    日期：2017-03-24
    时间：03:36
    author:作死小蜜蜂
'''
import os
import hashlib
from rest_framework.response import Response

def rand_str(length=32):
    if length > 128:
        raise ValueError("length must <= 128")
    return hashlib.sha512(os.urandom(128)).hexdigest()[0:length]

def error_response(error_reason):
    return Response(data={"code": 1, "data": error_reason})

def serializer_invalid_response(serializer):
    return error_response("字段验证失败")

def success_response(data):
    return Response(data={"code": 0, "data": data})