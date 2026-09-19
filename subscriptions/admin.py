from django.contrib import admin
from .models import Plan, Subscription, Payment



@admin.register
class PlanAdmin(admin.ModelAdmin):
     list_display = ('title', 'price', 'duration_days', 'is_active')

@admin.register
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'end_date')
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    