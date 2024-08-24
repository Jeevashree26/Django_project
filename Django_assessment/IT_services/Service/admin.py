from django.contrib import admin
from .models import Service,Subscription

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'active')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'address', 'payment_status', 'transaction_id', 'amount', 'created_at')
    search_fields = ('user__username', 'service__name', 'transaction_id')