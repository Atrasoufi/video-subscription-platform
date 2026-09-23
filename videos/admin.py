# videos/admin.py
from django.contrib import admin
from .models import Video, WatchHistory


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'duration', 'is_premium', 'created_at')
    list_filter = ('is_premium', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('uploader',)


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'progress', 'is_completed', 'watched_at')
    list_filter = ('is_completed', 'watched_at')
    search_fields = ('user__email', 'video__title')
    readonly_fields = ('created_at', 'watched_at')
    list_select_related = ('user', 'video')