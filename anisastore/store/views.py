from django.shortcuts import render
from django.http import HttpResponse
from . import models

# Custom View
from django.views import View
# Generic View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView


class ProductListView(ListView):
    model = models.Product
    template_name = 'store/product_list.html'
    paginate_by = 9

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(enabled=True)

# Create your views here.
