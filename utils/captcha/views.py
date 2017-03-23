#-*- coding:utf-8 -*-
'''
    日期：2017-03-24
    时间：03:33
    author:作死小蜜蜂
'''
from django.http import HttpResponse

from utils.captcha import Captcha


def show_captcha(request):
    return HttpResponse(Captcha(request).display(), content_type="image/gif")
