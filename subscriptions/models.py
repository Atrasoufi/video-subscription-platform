from django.db import models
# from accounts.models import CustomUser
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


class Plan(models.Model):
    title = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    is_active = models.BooleanField()
    
    def __str__(self):
        return f"{self.title} - {self.price}"
    
    
class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="subscriptions")
    
    
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)


    
    def __str__(self):
        return f"{self.user} - {self.plan.title}"
    
    
class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "در انتظار پرداخت"
        SUCCESSFUL = "SUCCESSFUL", "موفق"
        FAILED = "FAILED", "ناموفق"

        
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="payments",
)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    # subscription = models.ForeignKey(Subscription)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default='PENDING')
    tracking_code = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"

    
    
