from django.db import models
from mptt.models import MPTTModel
from mptt.managers import TreeManager
from django.db.models import Manager
from versatileimagefield.fields import PPOIField,VersatileImageField
from django.utils import timezone

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

class CartItem(models.Model):
    product = models.ForeignKey(Product)
    num = models.IntegerField(default=0)

    def get_price(self):
        return self.product.price * self.num

class Cart(models.Model):
    cartitems = models.ManyToManyField(CartItem)

    def total_price(self):
        prices = 0.0
        for cartitem in self.cartitems.all():
            prices += cartitem.get_price()
        return prices

    def add_item(self, productid, num):
        for cartitem in self.cartitems.all():
            if cartitem.product.id == productid:
                if cartitem.product.num < num:
                    return False
                cartitem.product.num -= num
                cartitem.product.save()

                cartitem.num += num
                cartitem.save()
                return True
        try:
            product = Product.objects.get(pk=productid)
        except Product.DoesNotExist:
            return False
        cartitem = CartItem(product=product, num=num)
        cartitem.save()
        self.cartitems.add(cartitem)
        self.save()
        return True

    def add_item_from_cart(self, cart_id, num):
        for cartitem in self.cartitems.all():
            if cartitem.id == cart_id:

                if cartitem.product.num < num:
                    raise ValueError()

                cartitem.product.num -= num
                cartitem.product.save()

                cartitem.num += num
                cartitem.save()
                return cartitem.num, cartitem.get_price()
        return (0, 0)


    def dec_item_from_cart(self, cart_id, num):
        for cartitem in self.cartitems.all():
            if cartitem.id == cart_id:
                if cartitem.num == 0:
                    return (0, 0)
                cartitem.num -= num

                cartitem.product.num += num
                cartitem.product.save()

                if cartitem.num == 0:
                    self.cartitems.remove(cartitem)
                    cartitem.delete()
                    return (0, 0)
                cartitem.save()
                return cartitem.num, cartitem.get_price()
        return (0, 0)

    def delete_item(self, cart_id):
        for cartitem in self.cartitems.all():
            if cartitem.id == cart_id:
                cartitem.product.num += cartitem.num
                cartitem.product.save()
                cartitem.delete()
                return True

        return False

    def dec_item_num(self, productid, num):
        for cartitem in self.cartitems.all():
            if cartitem.product.get_id() == productid:
                cartitem.num -= num
                cartitem.product.num += num
                cartitem.product.save()
                if cartitem.num < 0:
                    cartitem.num = 0
                cartitem.save()
                return True

        return False

    def clear(self):
        for cartitem in self.cartitems.all():
            cartitem.product.num += cartitem.num
            cartitem.product.save()
            self.cartitems.remove(cartitem)
            cartitem.delete()


class Invoice(models.Model):
    type = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=600)

class Order(models.Model):
    items = models.ManyToManyField(CartItem)
    address = models.ForeignKey('account.Address')
    status = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_created=True,default=timezone.now)
    notice = models.CharField(max_length=600,blank=True)
    invoice = models.ForeignKey(Invoice,blank=True,null=True)

