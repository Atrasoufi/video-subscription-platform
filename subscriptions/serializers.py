# subscriptions/serializers.py
from rest_framework import serializers
from .models import Plan, Subscription, Payment


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'id',
            'name',
            'description',
            'price',
            'duration_days',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_details = PlanSerializer(source='plan', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'plan',
            'price',
            'start_date',
            'end_date',
            'is_active',
        ]
        read_only_fields = ['id', 'start_date', 'end_date', 'is_active']
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'plan',
            'subscription',
            'amount',
            'status',
            'tracking_code',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']