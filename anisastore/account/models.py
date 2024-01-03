from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid
from django.utils import timezone
from django.core.validators import ValidationError
from django.core.validators import FileExtensionValidator


# from django.contrib.auth.models import User


def _get_avatar_path(obj, file):
    name = uuid.uuid4()
    ext = os.path.splitext(file)[1].lower()
    path = timezone.now().strftime('product_image/%Y/%m/%d/')
    return os.path.join(path, f'{name}{ext}')


def _image_dims_validator(image):
    if image.height > 100 or image.width > 100:
        raise ValidationError("size must be less than 100*100")


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to=_get_avatar_path, null=True, blank=True,
                               validators=[FileExtensionValidator(['jpg', 'png']),
                                           _image_dims_validator])
    email = models.EmailField('email address')
