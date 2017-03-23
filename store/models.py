from django.db import models
from mptt.models import MPTTModel
from mptt.managers import TreeManager
from django.db.models import Manager
from versatileimagefield.fields import PPOIField,VersatileImageField

# Create your models here.

class Category(MPTTModel):
    name = models.CharField("分类",max_length=128)
    description = models.CharField("描述",max_length=128)
    parent = models.ForeignKey('self',null=True,blank=True,related_name='children',
                               verbose_name="父类")

    objects = Manager()
    tree = TreeManager()

    class Meta:
        verbose_name="分类"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField("品牌",max_length=128)
    index = models.IntegerField("排序",default=1)

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Size(models.Model):
    size_choices = ((0,"S"),(1,"M"),(2,"L"),(3,"XL"),(4,"XXL"),(5,"XXXL"),(6,"4XL"))
    name  = models.IntegerField("尺寸",choices=size_choices)
    index = models.IntegerField("排序",default=1)

    class Meta:
        verbose_name = "尺寸"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.size_choices[self.name][1]

class Tag(models.Model):
    name = models.CharField("标签",max_length=128)
    index = models.IntegerField("排序",default=1)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProductManager, self).get_queryset().filter(active=True)

class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name="名称")
    brand = models.ForeignKey(Brand, verbose_name="品牌")
    size = models.ManyToManyField(Size, verbose_name="大小")
    price = models.FloatField(default=0, verbose_name="原价")
    discount = models.FloatField(default=0, verbose_name="折扣")
    sales = models.IntegerField(default=0, verbose_name="销量")
    desc = models.CharField(max_length=128, verbose_name="描述")
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    num = models.IntegerField(default=0, verbose_name="库存")
    image = VersatileImageField(upload_to="product/%Y/%m",verbose_name="显示图片"
                                ,ppoi_field='ppoi')

    image_right = VersatileImageField(upload_to="product/%Y/%m", verbose_name="侧面图片",null=True
                                , ppoi_field='ppoi')

    image_back = VersatileImageField(upload_to="product/%Y/%m", verbose_name="背部图片",null=True
                                , ppoi_field='ppoi')

    ppoi = PPOIField('image PPOI')
    categories = models.ManyToManyField(Category, verbose_name="分类")
    active = models.BooleanField(default=True, verbose_name="是否有效")

    objects = Manager()
    active_objects = ActiveProductManager()

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name
        ordering = ['id', ]

    def get_first_category(self):
        for category in self.categories.all():
            return category
        return None

    def __str__(self):
        return self.name

