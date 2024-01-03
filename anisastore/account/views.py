from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as DJ_LoginView
from . import forms
from django.views import View


# Create your views here.
class SignupView(View):
    def get(self, request):
        form = forms.SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_active = False
            obj.save()
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})
