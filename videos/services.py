from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_video_update(video_id, user_email, progress):
 
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'video_updates',
        {
            'type': 'video_update',
            'data': {
                'event': 'watch_progress',
                'video_id': video_id,
                'user': user_email,
                'progress': progress,
            }
        }
    )