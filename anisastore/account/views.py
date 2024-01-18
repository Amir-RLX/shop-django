from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as DJ_LoginView
from . import forms, models
from django.views import View
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string


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
            send_activation_email(request, obj)
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})


class ActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}"


TOKEN_GENERATOR = ActivationTokenGenerator()


def send_activation_email(request, user):
    template = 'registration/activation_email.html'
    to = user.email
    token = TOKEN_GENERATOR.make_token(user=user)
    uid = urlsafe_base64_encode(str(user.pk).encode('utf8'))
    site = get_current_site(request=request)
    domain = site.domain
    path = reverse('activate', kwargs={'uid': uid, 'token': str(token)})
    url = f'http://{domain}{path}'
    content = render_to_string(template_name=template, context={'url': url, 'user': user})
    subject = 'Activation'
    mail = EmailMessage(subject=subject, body=content, to=[to])
    mail.send()


class ActivateView(View):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode('utf8')
            user = models.User.objects.get(pk=pk)
        except (ValueError, models.User.DoesNotExist) as e:
            user = None
        if user is not None and TOKEN_GENERATOR.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return render(request, 'registration/activation_failed.html')
