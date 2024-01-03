from django.shortcuts import render
from django.http import HttpResponse
from . import models
from . import forms

# Custom View
from django.views import View
# Generic View
from django.views.generic import ListView
# from django.views.generic import DetailView
# from django.views.generic import TemplateView


# Create your views here.

class ProductListView(ListView):
    model = models.Product
    template_name = 'store/product_list.html'
    paginate_by = 9

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(enabled=True)


class ContactUsView(View):
    def get(self, request):
        form = forms.ContactusForm()
        return render(request=request, template_name='store/contact_us.html', context={'form': form})

    def post(self, request):
        form = forms.ContactusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            ...
        else:
            return render(request=request, template_name='store/contact_us.html', context={'form': form})


class ViewProduct(View):
    def get(self, request):
        comment_form = forms.CommentForm()
        # return render(request,template_name='store/product.html',context={"form":comment_form})
        ...


class CommentView(View):
    def post(self, request):
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            # obj = form.save()
            obj = form.save(commit=False)
            obj.user = request.user
            obj.product = ...
            obj.save()
            ...
        else:
            return render(request=request, template_name='store/contact_us.html', context={'form': form})
