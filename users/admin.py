from django.contrib import admin
from .models import AccessToken


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('key', 'description')
    readonly_fields = ('key', 'created_at')
    ordering = ('-created_at',)