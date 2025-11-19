"""
Billing URLs
URLs para billing e pagamentos
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlanViewSet,
    SubscriptionViewSet,
    InvoiceViewSet,
    PaymentViewSet,
    PaymentMethodViewSet,
    stripe_webhook,
)

router = DefaultRouter()
router.register(r"plans", PlanViewSet, basename="plan")
router.register(r"subscriptions", SubscriptionViewSet, basename="subscription")
router.register(r"invoices", InvoiceViewSet, basename="invoice")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"payment-methods", PaymentMethodViewSet, basename="payment-method")

urlpatterns = [
    path("", include(router.urls)),
    path("webhooks/stripe/", stripe_webhook, name="billing-stripe-webhook"),
]

