from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError
import re
from . import models

PHONE_REGEX = re.compile(r'^(\+98|0|0098)?9\d{9}$')


class ContactusForm(forms.Form):
    name = forms.CharField(required=True, label="Your Name")
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
    age = forms.IntegerField(validators=[MinValueValidator(18, message="Age Must Be More Than 18"),
                                         MaxValueValidator(50, message="Age Must Be Less Than 50")])
    message = forms.CharField(widget=forms.Textarea, help_text="Enter Your Message")

    def clean_phone(self):
        phone = self.cleaned_data.get('phone').strip()
        if not PHONE_REGEX.search(phone):
            raise ValidationError("Phone is invalid")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise ValidationError("We Only Accept Gmails")
        return email

    def clean(self):
        r = super(ContactusForm, self).clean()
        if not self.cleaned_data.get('phone') and not self.cleaned_data.get('email'):
            raise ValidationError('Phone or Email must be filled')
        return r


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        # fields = '__all__'
        fields = ['body']
        # exclude = ['user', 'product']
