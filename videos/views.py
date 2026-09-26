from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Video, WatchHistory
from .serializers import (
    VideoSerializer,
    VideoListSerializer,
    WatchHistorySerializer,
    WatchHistoryCreateSerializer,
)
from .services import broadcast_video_update
from subscriptions.permissions import HasActiveSubscription


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.select_related('uploader').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return VideoListSerializer
        return VideoSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated(), HasActiveSubscription()]
        # list is public
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated()],
    )
    def watch(self, request, pk=None):

        video = self.get_object()
        serializer = WatchHistoryCreateSerializer(data={
            'video': video.id,
            'progress': request.data.get('progress', 0),
            'is_completed': request.data.get('is_completed', False),
        })
        serializer.is_valid(raise_exception=True)

        history, _ = WatchHistory.objects.update_or_create(
            user=request.user,
            video=video,
            defaults={
                'progress': serializer.validated_data['progress'],
                'is_completed': serializer.validated_data['is_completed'],
            }
        )

        # Broadcast live update to all connected WebSocket clients
        broadcast_video_update(
            video_id=video.id,
            user_email=request.user.email,
            progress=history.progress,
        )

        return Response(
            WatchHistorySerializer(history).data,
            status=status.HTTP_200_OK
        )


class WatchHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = WatchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchHistory.objects.filter(
            user=self.request.user
        ).select_related('video')

    def get_serializer_class(self):
        if self.action == 'create':
            return WatchHistoryCreateSerializer
        return WatchHistorySerializer

    def perform_create(self, serializer):
        video = serializer.validated_data['video']
        progress = serializer.validated_data.get('progress', 0)
        is_completed = serializer.validated_data.get('is_completed', False)

        history, _ = WatchHistory.objects.update_or_create(
            user=self.request.user,
            video=video,
            defaults={'progress': progress, 'is_completed': is_completed}
        )
        serializer.instance = history