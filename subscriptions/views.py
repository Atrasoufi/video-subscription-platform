from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.utils.crypto import get_random_string

from .models import Plan, Subscription, Payment
from .serializers import (
    PlanSerializer,
    SubscriptionSerializer,
    SubscriptionCreateSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
)


class PlanViewSet(viewsets.ModelViewSet):

    queryset = Plan.objects.filter(is_active=True)

    def get_serializer_class(self):
        return PlanSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class SubscriptionViewSet(viewsets.ModelViewSet):
  
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(
            user=self.request.user
        ).select_related('plan', 'user')

    def get_serializer_class(self):
        if self.action == 'create':
            return SubscriptionCreateSerializer
        return SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        return Response(
            SubscriptionSerializer(subscription).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Deactivate a subscription (soft cancel)."""
        subscription = self.get_object()
        subscription.is_active = False
        subscription.save(update_fields=['is_active'])
        return Response(
            {"detail": "Subscription cancelled."},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Return the user's current active subscription."""
        sub = self.get_queryset().filter(
            is_active=True,
            end_date__gte=timezone.now().date()
        ).first()

        if not sub:
            return Response(
                {"detail": "No active subscription."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(SubscriptionSerializer(sub).data)


class PaymentViewSet(viewsets.ModelViewSet):

    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            user=self.request.user
        ).select_related('plan', 'subscription')

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        """Step 1: create a pending payment."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
  
        payment = self.get_object()

        if payment.status != Payment.StatusChoices.PENDING:
            return Response(
                {"detail": "Payment already processed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = request.data.get('status', 'SUCCESSFUL').upper()

        if result == 'FAILED':
            payment.status = Payment.StatusChoices.FAILED
            payment.save(update_fields=['status'])
            return Response(
                {"detail": "Payment failed."},
                status=status.HTTP_200_OK
            )

        # Simulate successful payment
        payment.status = Payment.StatusChoices.SUCCESSFUL
        payment.tracking_code = get_random_string(12).upper()
        payment.save(update_fields=['status', 'tracking_code'])

        # Create subscription
        subscription = Subscription.objects.create(
            user=request.user,
            plan=payment.plan,
            price=payment.amount,
        )
        payment.subscription = subscription
        payment.save(update_fields=['subscription'])

        return Response(
            {
                "detail": "Payment successful.",
                "tracking_code": payment.tracking_code,
                "subscription": SubscriptionSerializer(subscription).data,
            },
            status=status.HTTP_200_OK
        )