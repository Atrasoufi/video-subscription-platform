from django.db import models
from django.conf import settings


class Video(models.Model):
    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    video_file = models.FileField(
        upload_to="videos/",
        blank=True,
        null=True
    )

    video_url = models.URLField(
        blank=True,
        null=True
    )

    thumbnail = models.ImageField(
        upload_to="thumbnails/",
        blank=True,
        null=True
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in seconds"
    )

    is_premium = models.BooleanField(default=True)

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_videos"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class WatchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watch_history"
    )

    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name="watched_by"
    )

    progress = models.PositiveIntegerField(
        default=0,
        help_text="Progress in seconds"
    )

    is_completed = models.BooleanField(default=False)

    watched_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "video")
        ordering = ["-watched_at"]
        verbose_name_plural = "Watch histories"

    def __str__(self):
        return f"{self.user.email} - {self.video.title} ({self.progress}s)"