from rest_framework import serializers
from .models import Video, WatchHistory


class VideoSerializer(serializers.ModelSerializer):

    uploader_email = serializers.EmailField(
        source='uploader.email', read_only=True
    )

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description',
            'video_file', 'video_url', 'thumbnail',
            'duration', 'is_premium',
            'uploader', 'uploader_email',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['uploader', 'created_at', 'updated_at']


class VideoListSerializer(serializers.ModelSerializer):

    uploader_email = serializers.EmailField(
        source='uploader.email', read_only=True
    )

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'thumbnail', 'duration',
            'is_premium', 'uploader_email', 'created_at',
        ]


class WatchHistorySerializer(serializers.ModelSerializer):
   
    video_title = serializers.CharField(source='video.title', read_only=True)
    video_thumbnail = serializers.ImageField(
        source='video.thumbnail', read_only=True
    )
    video_duration = serializers.IntegerField(
        source='video.duration', read_only=True
    )

    class Meta:
        model = WatchHistory
        fields = [
            'id', 'video', 'video_title', 'video_thumbnail',
            'video_duration', 'progress', 'is_completed',
            'watched_at', 'created_at',
        ]
        read_only_fields = ['watched_at', 'created_at']


class WatchHistoryCreateSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = WatchHistory
        fields = ['video', 'progress', 'is_completed']

    def validate(self, attrs):
        video = attrs.get('video')
        progress = attrs.get('progress', 0)

        if video and progress > video.duration:
            raise serializers.ValidationError(
                {"progress": "Progress cannot exceed video duration."}
            )
        return attrs