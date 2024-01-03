from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe


# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'get_avatar', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']

    @admin.display(description='Avatar')
    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src = "{obj.avatar.url}" />')
        return '-'
