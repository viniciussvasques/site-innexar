"""
Billing Serializers
Serializers para planos, assinaturas, faturas e pagamentos
"""
from rest_framework import serializers
from decimal import Decimal
from .models import Plan, Subscription, Invoice, Payment, PaymentMethod
from apps.tenants.models import Tenant


class PlanSerializer(serializers.ModelSerializer):
    """Serializer para Plan"""
    
    # Preços formatados para exibição
    price_monthly_display = serializers.SerializerMethodField()
    price_yearly_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Plan
        fields = [
            'id', 'name', 'slug', 'description',
            'price_monthly_brl', 'price_yearly_brl',
            'price_monthly_usd', 'price_yearly_usd',
            'price_monthly_display', 'price_yearly_display',
            'currency', 'max_projects', 'max_users', 'max_storage_gb',
            'features', 'is_active', 'is_featured', 'trial_days',
            'display_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_price_monthly_display(self, obj):
        """Retorna preço mensal formatado baseado no país do tenant"""
        request = self.context.get('request')
        if request and hasattr(request, 'user') and hasattr(request.user, 'tenant') and request.user.tenant:
            country = request.user.tenant.country
        else:
            country = 'BR'  # Default
        price = obj.get_price_for_country(country, 'monthly')
        currency_symbol = 'R$' if country == 'BR' else '$'
        return f"{currency_symbol} {price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def get_price_yearly_display(self, obj):
        """Retorna preço anual formatado baseado no país do tenant"""
        request = self.context.get('request')
        if request and hasattr(request, 'user') and hasattr(request.user, 'tenant') and request.user.tenant:
            country = request.user.tenant.country
        else:
            country = 'BR'  # Default
        price = obj.get_price_for_country(country, 'yearly')
        currency_symbol = 'R$' if country == 'BR' else '$'
        return f"{currency_symbol} {price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


class PaymentMethodSerializer(serializers.ModelSerializer):
    """Serializer para PaymentMethod"""
    
    card_display = serializers.SerializerMethodField()
    
    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'type', 'gateway', 'is_default', 'is_active',
            'card_last4', 'card_brand', 'card_exp_month', 'card_exp_year',
            'card_display', 'billing_details', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'gateway_payment_method_id', 'created_at', 'updated_at']
    
    def get_card_display(self, obj):
        """Retorna exibição formatada do cartão"""
        if obj.type == 'card' and obj.card_last4:
            brand = obj.get_card_brand_display() if obj.card_brand else 'Cartão'
            return f"{brand} •••• {obj.card_last4}"
        return None


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer para Subscription"""
    
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.filter(is_active=True),
        source='plan',
        write_only=True
    )
    payment_method = PaymentMethodSerializer(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_trial = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'tenant', 'plan', 'plan_id', 'status',
            'current_period_start', 'current_period_end',
            'trial_start', 'trial_end', 'is_trial',
            'cancel_at_period_end', 'canceled_at', 'cancellation_reason',
            'gateway', 'gateway_subscription_id', 'payment_method',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'tenant', 'status', 'gateway_subscription_id',
            'gateway_customer_id', 'created_at', 'updated_at'
        ]


class InvoiceLineItemSerializer(serializers.Serializer):
    """Serializer para itens da fatura"""
    description = serializers.CharField()
    quantity = serializers.IntegerField(default=1)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer para Invoice"""
    
    subscription = SubscriptionSerializer(read_only=True)
    line_items = InvoiceLineItemSerializer(many=True, required=False)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'tenant', 'subscription', 'invoice_number',
            'amount', 'currency', 'tax_amount', 'total_amount',
            'status', 'status_display', 'issue_date', 'due_date', 'paid_at',
            'gateway_invoice_id', 'gateway_pdf_url', 'line_items', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'tenant', 'invoice_number', 'gateway_invoice_id',
            'gateway_pdf_url', 'paid_at', 'created_at', 'updated_at'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer para Payment"""
    
    invoice = InvoiceSerializer(read_only=True)
    payment_method = PaymentMethodSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_type_display = serializers.CharField(source='get_payment_method_type_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'invoice', 'tenant', 'payment_method', 'amount', 'currency',
            'status', 'status_display', 'payment_method_type', 'payment_method_type_display',
            'gateway', 'gateway_payment_id', 'gateway_charge_id',
            'failure_reason', 'retry_count', 'max_retries', 'metadata',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'tenant', 'gateway_payment_id', 'gateway_charge_id',
            'created_at', 'updated_at'
        ]


# Serializers para ações específicas

class CreateSubscriptionSerializer(serializers.Serializer):
    """Serializer para criar assinatura"""
    plan_id = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.filter(is_active=True))
    payment_method_id = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethod.objects.all(),
        required=False,
        allow_null=True
    )
    billing_cycle = serializers.ChoiceField(choices=['monthly', 'yearly'], default='monthly')


class UpgradeSubscriptionSerializer(serializers.Serializer):
    """Serializer para upgrade de assinatura"""
    plan_id = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.filter(is_active=True))


class CancelSubscriptionSerializer(serializers.Serializer):
    """Serializer para cancelar assinatura"""
    reason = serializers.CharField(required=False, allow_blank=True)


class CreatePaymentMethodSerializer(serializers.Serializer):
    """Serializer para criar método de pagamento"""
    type = serializers.ChoiceField(choices=['card', 'boleto', 'pix'])
    token = serializers.CharField(help_text='Token do gateway (obtido no frontend)')
    is_default = serializers.BooleanField(default=False)
    billing_details = serializers.JSONField(required=False, default=dict)

