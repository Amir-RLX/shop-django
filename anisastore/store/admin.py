from django.contrib import admin
from . import models


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)
    list_display = ('name', 'count', 'price', 'category', 'enabled')
    list_filter = ('category',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    ...


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
