from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    context = {}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {}
    return render(request, template, context)

def show_catalog(request):
    sort_type = request.GET.get('sort', 'name')  # 'name' — сортировка по умолчанию

    if sort_type == 'name':
        phones = Phone.objects.all().order_by('name')
    elif sort_type == 'min_price':
        phones = Phone.objects.all().order_by('price')
    elif sort_type == 'max_price':
        phones = Phone.objects.all().order_by('-price')  # Минус перед полем означает убывание
    else:
        phones = Phone.objects.all()

    context = {'phones': phones}
    return render(request, 'catalog.html', context)
