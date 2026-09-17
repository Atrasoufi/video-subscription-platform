from django.db import models
# from accounts.models import CustomUser
from django.conf import settings
class Plan(models.Model):
    title = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    is_active = models.BooleanField()
    
    def __str__(self):
        return f"{self.title} - {self.price}"
    
    
class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f"{self.user} - {self.plan.title}"
    
    
class Payment(models.Model):
    user = models.ForeignKey(
    CustomUser,
    on_delete=models.CASCADE
)
    subscription = models.ForeignKey(Subscription)
    amount = models.DecimalField()
    status = models.BooleanField()
    tracking_code = models.IntegerField()
    
    
