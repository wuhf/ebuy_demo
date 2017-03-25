from django.shortcuts import render
from .models import Product, Category, Cart
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from store import forms
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from .serializers import *
from utils.utils import *


# Create your views here.
def index(request):
    clo_list = Product.objects.all()
    clo_list = get_page(request, clo_list)
    categories = Category.objects.filter(parent=None)
    search_form = forms.SearchForm()
    return render(request, "store/index.html", locals())


def get_page(request, clo_list):
    paginator = Paginator(clo_list, 4)
    try:
        page = int(request.GET.get('page', 1))
        clo_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        clo_list = paginator.page(1)
    return clo_list


def product(request, id):
    try:
        clo = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return render(request, 'error.html', {'error': "商品不存在"})

    return render(request, 'store/product.html', locals())


def categpries(request, id):
    try:
        cat = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        return render(request, 'error.html', {'error': '分类不存在'})

    clo_list = Product.active_objects.filter(categories=cat)
    clo_list = get_page(request, clo_list)
    categories = Category.objects.filter(parent=None)
    return render(request, 'store/index.html', locals())


def search(request):
    categories = Category.objects.filter(parent=None)
    search_form = forms.SearchForm(request.GET)
    if search_form.is_valid():
        keyword = search_form.cleaned_data['keyword']
        query = SearchQuerySet()
        sqs = query.auto_query(keyword)
        clo_list = []
        for s in sqs:
            clo = Product.objects.get(pk=s.pk)
            if clo:
                clo_list.append(clo)

        clo_list = get_page(request, clo_list)
    return render(request, "store/index.html", locals())


@login_required
def view_cart(request):
    try:
        cart = request.user.userprofile.cart
    except:
        cart = Cart()
        cart.save()
        request.user.userprofile.cart = cart
        request.user.userprofile.save()
    return render(request, 'store/cart.html', locals())


class AddProductToCartView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        serializer = AddItemtoCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.data['product_id']
            try:
                product = Product.objects.get(pk=product_id)
                if product.num < 1:
                    return error_response('产品库存不足!')
            except Product.DoesNotExist:
                return error_response('产品不存在')

            cart = request.user.userprofile.cart
            cart.add_item(product_id, 1)
            return success_response('添加成功')

        return serializer_invalid_response(serializer)


class CartItemOpView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        serializer = CartItemOpSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            cart_id = data['cart_id']
            is_add = data['is_add']
            cart = request.user.userprofile.cart
            if is_add:
                try:
                    res_num, item_price = cart.add_item_from_cart(cart_id, 1)
                except ValueError:
                    return error_response("产品数量不足")
            else:
                res_num, item_price = cart.dec_item_from_cart(cart_id, 1)

            return success_response({'res_num':res_num, 'item_price':item_price
                                     , 'total_price':cart.total_price()})

        return serializer_invalid_response(serializer)

class DeleteCartItemView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        serializer = DeleteCartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart_id = serializer.data['cart_id']
            cart = request.user.userprofile.cart
            if cart.delete_item(cart_id):
                return success_response(cart.total_price())

            return error_response('failed')

        return serializer_invalid_response(serializer)

class CartClearView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        cart = request.user.userprofile.cart
        cart.clear()

        return success_response('success')