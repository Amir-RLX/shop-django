from django.urls import path, include
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('contactus', views.ContactUsView.as_view(), name='contactus'),

]
