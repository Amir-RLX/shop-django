from . import views
from django.urls import path, include

urlpatterns = [
    path('signup',views.SignupView.as_view(),name='signup')
]

