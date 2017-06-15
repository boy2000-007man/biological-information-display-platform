from django.contrib import admin

# Register your models here.
from .models import upload

class uploadAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime'

    readonly_fields = upload._meta.get_all_field_names()

    list_filter = [
        'username',
        'datetime',
        'action'
    ]

    search_fields = [
        'username',
        'datetime',
        'action'
    ]

    list_display = [
        'username',
        'datetime',
        'action'
    ]
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
        
admin.site.register(upload, uploadAdmin)
