from django.utils import timezone
from rest_framework import permissions


class HasActiveSubscription(permissions.BasePermission):

    message = "You need an active subscription to access this content."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Staff users bypass subscription check
        if user.is_staff:
            return True

        return user.subscriptions.filter(
            is_active=True,
            end_date__gte=timezone.now().date()
        ).exists()