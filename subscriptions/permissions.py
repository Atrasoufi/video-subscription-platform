from rest_framework import permissions


class HasActiveSubscription(permissions.BasePermission):


    message = "You need an active subscription to access this content."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        
        if user.is_staff:
            return True

        
        return user.subscriptions.filter(
            is_active=True,
            end_date__gte=__import__('django.utils.timezone', fromlist=['now']).now().date()
        ).exists()