from django.contrib import admin
from .models import Plan, Subscription, Payment


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'end_date')
    search_fields = ('user__email', 'plan__title')
    list_select_related = ('user', 'plan')
    readonly_fields = ('start_date',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'plan__title', 'tracking_code')
    list_select_related = ('user', 'plan', 'subscription')
    readonly_fields = ('created_at',)