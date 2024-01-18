from . import views
from django.urls import path, include

urlpatterns = [
    path('signup',views.SignupView.as_view(),name='signup'),
    path('activate/<str:uid>/<str:token>', views.ActivateView.as_view(), name='activate'),

]

