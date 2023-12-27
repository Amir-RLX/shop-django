from django.db import models


# Create your models here.


class Product(models.Model):
    # django automatically adds a column for "id"
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    description = models.TextField()
