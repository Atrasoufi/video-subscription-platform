from rest_framework import serializers
from django.utils import timezone
from .models import Plan, Subscription, Payment


class PlanSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Plan
        fields = ['id', 'title', 'price', 'duration_days', 'is_active']


class SubscriptionSerializer(serializers.ModelSerializer):
    
    plan = PlanSerializer(read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'user_email', 'plan', 'price',
            'start_date', 'end_date', 'is_active',
            'is_valid',
        ]
        read_only_fields = ['price', 'start_date', 'end_date']


class SubscriptionCreateSerializer(serializers.ModelSerializer):
   
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.filter(is_active=True),
        source='plan',
        write_only=True,
    )

    class Meta:
        model = Subscription
        fields = ['id', 'plan_id']

    def validate(self, attrs):
        user = self.context['request'].user
        plan = attrs['plan']

        # Prevent duplicate active subscription
        has_active = user.subscriptions.filter(
            is_active=True,
            end_date__gte=timezone.now().date()
        ).exists()

        if has_active:
            raise serializers.ValidationError(
                {"detail": "You already have an active subscription."}
            )
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        plan = validated_data['plan']
        return Subscription.objects.create(
            user=user,
            plan=plan,
            price=plan.price,
        )


class PaymentSerializer(serializers.ModelSerializer):
    
    plan_title = serializers.CharField(source='plan.title', read_only=True)
    status_display = serializers.CharField(
        source='get_status_display', read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            'id', 'plan', 'plan_title', 'subscription',
            'amount', 'status', 'status_display',
            'tracking_code', 'created_at',
        ]
        read_only_fields = [
            'plan', 'subscription', 'amount',
            'status', 'tracking_code', 'created_at',
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.filter(is_active=True),
        source='plan',
        write_only=True,
    )

    class Meta:
        model = Payment
        fields = ['id', 'plan_id']

    def create(self, validated_data):
        user = self.context['request'].user
        plan = validated_data['plan']
        return Payment.objects.create(
            user=user,
            plan=plan,
            amount=plan.price,
            status=Payment.StatusChoices.PENDING,
        )