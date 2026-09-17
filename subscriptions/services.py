from datetime import timedelta
from django.utils import timezone
from .models import Subscription

def create_user_subscription(user, plan):
    if not plan.is_active:
        raise ValueError("Cannot subscribe to an inactive plan")
    
    start_date = timezone.now()
    end = start_date + timedelta(days=plan.duration_days)
    
    return Subscription.objects.create(
        user=user,
        plan=plan,
        start_date=start_date,
        end_date=end,
        is_active=True,
    )
