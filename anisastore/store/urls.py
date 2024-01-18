from django.urls import path, include
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('contactus', views.ContactUsView.as_view(), name='contactus'),
    path('product/<int:pk>/<str:slug>', views.ContactUsView.as_view(), name='contactus'),
    path('cart/add/<uuid:pk>', views.CartAddView.as_view(), name='cart_add'),
    path('cart', views.CartView.as_view(), name='cart_view'),
    path('invoice/<int:pk>', views.InvoiceView.as_view(), name='invoice_view'),
    path('invoice/<int:pk>/pay', views.PayView.as_view(), name='pay_view'),
    path('payment_verify', views.PayVerifyView.as_view(), name='pay_verify_view'),
    path('api/products',views.ProductListApiView.as_view(),name="api-products"),
    path('api/products/<uuid:uuid>/comment', views.CommentAPIView.as_view(), name="api-comments")

]
