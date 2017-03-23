#-*- coding:utf-8 -*-
'''
    日期：2017-03-23
    时间：19:08
    author:作死小蜜蜂
'''
from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(label='', max_length=50,
                              widget=forms.TextInput(attrs={
                                  'id':'select'
                                  , 'placeholder':'请输入搜索内容'
                              }))