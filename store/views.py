from django.shortcuts import render
from .models import Product,Category
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from store import forms
from haystack.query import SearchQuerySet


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
        return render(request, 'error.html', {'error':'分类不存在'})

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