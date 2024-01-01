from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", 'get_avatar')

    @admin.display(description='Avatar')
    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src = "{obj.avatar.url}" />')
        return '-'


admin.site.register(models.Profile, ProfileAdmin)
