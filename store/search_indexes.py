#-*- coding:utf-8 -*-
'''
    日期：2017-03-23
    时间：19:25
    author:作死小蜜蜂
'''

from haystack import indexes
from .models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()