from django.shortcuts import render
from django.http import HttpResponse
from . import models


# Create your views here.
def product_list(request):
    # Must return HTTPResponse
    objs = models.Product.objects.all()
    context = {
        'products': objs
    }
    return render(request=request, template_name='product_list.html', context=context)
