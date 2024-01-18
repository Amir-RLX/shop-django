from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from . import forms

# Custom View
from django.views import View
# Generic View
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import zeep
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import response
from . import serializers
from rest_framework.permissions import AllowAny

# from django.views.generic import DetailView
# from django.views.generic import TemplateView

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
WSDL = 'https://sandbox.zarinpal.com/pg/services/WebGate/wsdl'
GW = 'https://sandbox.zarinpal.com/pg/StartPay/{}'
ZARINPAL = zeep.Client(WSDL)


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


@method_decorator(login_required, name='post')
class ViewProduct(View):
    def get(self, request):
        comment_form = forms.CommentForm()
        # return render(request,template_name='store/product.html',context={"form":comment_form})
        ...

    def post(self, request):
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


class CartAddView(View):
    def get(self, request, pk):
        obj = get_object_or_404(models.Product, pk=pk, enabled=True)
        if 'cart' in request.session and request.session['cart']:
            cart = request.session['cart']
        else:
            cart = {'total_items_count': 0, 'items': {}}
        id = str(pk)
        if id in cart['items']:
            cart['items'][id] += 1
        else:
            cart['items'][id] = 1
        cart['total_items_count'] = sum(cart['items'].values())
        request.session['cart'] = cart
        return JsonResponse(cart)


@method_decorator(login_required, name='post')
class CartView(View):
    def get(self, request):
        if 'cart' in request.session:
            cart = request.session['cart']
        else:
            cart = {'total_items_count': 0, 'items': {}}
        full_cart = []
        if cart and cart['items']:
            products = models.Product.objects.filter(pk__in=cart['items'].keys())
            for pk, count in cart['items'].items():
                obj = products.get(pk=pk)
                full_cart.append({
                    'obj': obj,
                    'count': count,
                    'total_price': obj.price * count
                })
            return render(request=request, template_name='store/cart.html', context={'cart': full_cart})

    def post(self, request):
        if 'cart' in request.session:
            cart = request.session['cart']
        else:
            cart = {'total_items_count': 0, 'items': {}}
        if not cart['items']:
            return redirect('store:product-list')
        full_cart = []
        products = models.Product.objects.filter(pk__in=cart['items'].keys())
        with transaction.atomic():
            invoice = models.Invoice.objects.create(user=request.user)
            items = []
            total = 0
            for pk, count in cart['items'].items():
                obj = products.get(pk=pk)
                t = obj.price * count
                total += t
                item = models.InvoiceItem(invoice=invoice,
                                          count=count,
                                          product=obj,
                                          total=t,
                                          price=obj.price,
                                          name=obj.name)
                items.append(item)
            items = models.InvoiceItem.objects.bulk_create(items)
            invoice.total = total
            invoice.save()
        request.session['cart'] = None
        return redirect('store:invoice_view', pk=invoice.pk)


class InvoiceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def has_permission(self):
        obj = get_object_or_404(models.Invoice, pk=self.kwargs.get('pk'))
        return self.request.user == obj.user

    def get(self, request, pk):
        obj = get_object_or_404(models.Invoice, pk=pk)
        return render(request, 'store/invoice.html', {'obj': obj})


class PayView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def has_permission(self):
        obj = get_object_or_404(models.Invoice, pk=self.kwargs.get('pk'))
        return self.request.user == obj.user

    def post(self, request, pk):
        obj = get_object_or_404(models.Invoice, pk=pk)
        payment = models.Payment(invoice=obj,
                                 amount=obj.total)
        site = get_current_site(request=request)
        path = reverse('store:pay_verify_view')
        url = f"http://{site.domain}{path}"
        res = ZARINPAL.service.PaymentRequest(MERCHANT, payment.amount, "Some Products", '', '', url)
        if res.Status == 100:
            payment.authority = res.Authority
            payment.save()
            return redirect(GW.format(payment.authority))
        else:
            payment.state = payment.STATES.Error
            payment.gw_response = res.Status
            payment.save()
            return render(request, 'store/payment_error.html')


class PayVerifyView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def has_permission(self):
        return True

    def get(self, request):
        status = request.GET.get('Status')
        authority = request.GET.get('Authority')
        try:
            payment = models.Payment.objects.get(authority=authority,
                                                 state=models.Payment.STATES.PENDING)
            if status == 'OK':
                res = ZARINPAL.service.PaymentVerification(MERCHANT,
                                                           payment.authority, payment.amount)
                refid = res['RefID']
                if res['Status'] == 100:
                    payment.refid = refid
                    payment.state = models.Payment.STATES.PAID
                    payment.gw_response = res['Status']
                    payment.save()
                    payment.invoice.state = models.Invoice.STATES.PAID
                    payment.invoice.save()
                    return render(request, 'store/payment_done.html', {'refid': payment.refid})
                elif res['Status'] == 101:
                    if not payment.refid:
                        payment.refid = refid
                        payment.state = models.Payment.STATES.PAID
                        payment.gw_response = res['Status']
                        payment.save()
                        payment.invoice.state = models.Invoice.STATES.PAID
                        payment.invoice.save()
                        return render(request, 'store/payment_done.html', {'refid': payment.refid})
                    else:
                        messages.add_message(request, messages.ERROR, 'Invoice is already paid ')
                        return redirect('store:product-list')
                else:
                    payment.state = models.Payment.STATES.Error
                    payment.save()
                    messages.add_message(request, messages.ERROR, 'Payment Failed')
                    return redirect('store:invoice_view', pk=payment.invoice.pk)

            else:
                payment.state = models.Payment.STATES.Error
                payment.save()
                messages.add_message(request, messages.ERROR, 'Payment Canceled')
                return redirect('store:invoice_view', pk=payment.invoice.pk)
        except models.Payment.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Payment Not Found')
            return redirect('store:product-list')


class ProductListApiView(APIView):
    """
    Some Sample Api Page
    """

    def get(self, request):
        """
        List All Products
        :param request:
        :return:
        """
        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(data=serializer.data)


class CreatedResponse(response.Response):
    ...


class CommentAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uuid):
        product = get_object_or_404(models.Product, uuid=uuid)
        s = serializers.CommentSerializer(product.comments.all(), many=True)
        return Response(s.data)

    def post(self, request, uuid):
        product = get_object_or_404(models.Product, uuid=uuid)
        s = serializers.SubmitCommentSerializer(data=request.data)
        if s.is_valid(raise_exception=True):
            obj = s.save(user=request.user, product=product)
            s = serializers.CommentSerializer(obj)
            return Response(status=201, data=s.data)
