"""
Admin configuration for Billing models
"""
from django.contrib import admin
from .models import Plan, Subscription, Invoice, Payment, PaymentMethod


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price_monthly_brl', 'price_monthly_usd', 'max_projects', 'max_users', 'is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'currency']
    search_fields = ['name', 'slug', 'description']
    ordering = ['display_order', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'plan', 'status', 'current_period_start', 'current_period_end', 'gateway']
    list_filter = ['status', 'gateway', 'cancel_at_period_end']
    search_fields = ['tenant__name', 'plan__name', 'gateway_subscription_id']
    readonly_fields = ['created_at', 'updated_at', 'gateway_subscription_id', 'gateway_customer_id']
    date_hierarchy = 'current_period_start'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'tenant', 'total_amount', 'currency', 'status', 'due_date', 'paid_at']
    list_filter = ['status', 'currency']
    search_fields = ['invoice_number', 'tenant__name', 'gateway_invoice_id']
    readonly_fields = ['created_at', 'updated_at', 'invoice_number', 'gateway_invoice_id']
    date_hierarchy = 'issue_date'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'tenant', 'amount', 'currency', 'status', 'payment_method_type', 'gateway']
    list_filter = ['status', 'payment_method_type', 'gateway']
    search_fields = ['invoice__invoice_number', 'tenant__name', 'gateway_payment_id']
    readonly_fields = ['created_at', 'updated_at', 'gateway_payment_id', 'gateway_charge_id']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'type', 'card_brand', 'card_last4', 'is_default', 'is_active', 'gateway']
    list_filter = ['type', 'is_default', 'is_active', 'gateway']
    search_fields = ['tenant__name', 'gateway_payment_method_id', 'card_last4']
    readonly_fields = ['created_at', 'updated_at', 'gateway_payment_method_id']

