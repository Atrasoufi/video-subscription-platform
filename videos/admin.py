# videos/admin.py
from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'duration', 'is_premium', 'created_at')
    list_filter = ('is_premium', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('uploader',)