from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from .models import Subscription


class SubscriptionError(Exception):
    pass


@transaction.atomic
def create_user_subscription(user, plan):
    if not plan.is_active:
        raise ValueError("Cannot subscribe to an inactive plan")
    
    existing = user.subscriptions.filter(is_active=True).first()
    if existing and existing.is_valid():
        raise SubscriptionError("You already have an active subscription")
    
    
    
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=plan.duration_days)
    
    subscription = Subscription.objects.create(
        user=user,
        plan=plan,
        price=plan.price,
        duration_days = plan.duratioin.days,
        start_date=start_date,
        end_date=end_date,
        is_active=True,
    )

    return subscription
