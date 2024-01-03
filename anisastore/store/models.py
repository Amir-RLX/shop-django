from django.db import models
import uuid
from django.utils import timezone
import os
from django.core.validators import ValidationError
from django.core.validators import FileExtensionValidator
# from account.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

def _get_file_name(obj, file):
    name = uuid.uuid4()
    ext = os.path.splitext(file)[1].lower()
    path = timezone.now().strftime('product_image/%Y/%m/%d/')
    return os.path.join(path, f'{name}{ext}')


def image_dims_validator(image):
    if image.height > 500 or image.width > 500:
        raise ValidationError("size must be less than 500*500")


class Product(models.Model):
    # django automatically adds a column for "id"
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    description = models.TextField()
    enabled = models.BooleanField(default=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.PROTECT,
                                 related_name='products')
    image = models.ImageField(upload_to=_get_file_name, null=True, blank=True,
                              validators=[FileExtensionValidator(['jpg', 'png']),
                                          image_dims_validator])

    # def clean_image(self):
    #     if self.image.height > 500 or self.image.width > 500:
    #         raise ValidationError("size must be less than 500*500")
    #     return self.image

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ...
        return super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('Category',
                               on_delete=models.PROTECT,
                               null=True, blank=True,
                               related_name='childes')

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
