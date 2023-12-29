from django.db import models
import uuid


# Create your models here.


class Product(models.Model):
    # django automatically adds a column for "id"
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    description = models.TextField()
    category = models.ForeignKey('Category',
                                 on_delete=models.PROTECT,
                                 related_name='products')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('Category',
                               on_delete=models.PROTECT,
                               null=True, blank=True,
                               related_name='childes')

    def __str__(self):
        return self.name
