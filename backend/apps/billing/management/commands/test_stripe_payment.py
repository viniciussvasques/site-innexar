"""
Management command to perform a real Stripe test payment (TEST MODE).

Objetivo:
- Verificar se as chaves STRIPE_SECRET_KEY estão corretas
- Confirmar que o backend consegue criar um PaymentIntent de teste
- Validar o fluxo: Tenant (US) -> Plan (USD) -> Invoice -> PaymentService.process_payment

IMPORTANTE:
- Usa o método de pagamento de teste do Stripe: pm_card_visa
- NÃO gera nenhuma cobrança real (somente ambiente de teste do Stripe)
"""
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.billing.models import Plan, Tenant, Subscription, Invoice, PaymentMethod
from apps.billing.services import BillingService, InvoiceService, PaymentService


class Command(BaseCommand):
    help = "Executa um pagamento de teste real no Stripe (modo TESTE)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("🔄 Iniciando teste de pagamento Stripe (TEST MODE)"))

        # 1. Garantir tenant de teste (USA)
        tenant, _ = Tenant.objects.get_or_create(
            slug="stripe-test-tenant",
            defaults={
                "name": "Stripe Test Tenant",
                "domain": "stripe-test.structurone.com",
                "email": "stripe-test@example.com",
                "country": "US",
                "currency": "USD",
            },
        )
        self.stdout.write(self.style.SUCCESS(f"✅ Tenant de teste: {tenant.name} ({tenant.country})"))

        # 2. Garantir plano de teste em USD
        plan, _ = Plan.objects.get_or_create(
            slug="starter-us",
            defaults={
                "name": "Starter USA",
                "description": "Plano starter para teste com Stripe (USD).",
                "price_monthly_usd": Decimal("19.00"),
                "price_yearly_usd": Decimal("190.00"),
                "currency": "USD",
                "max_projects": 3,
                "max_users": 3,
                "max_storage_gb": 5,
                "features": ["Test plan for Stripe", "No real usage"],
                "is_active": True,
            },
        )
        self.stdout.write(self.style.SUCCESS(f"✅ Plano de teste: {plan.name} ({plan.slug})"))

        # 3. Criar método de pagamento Stripe de teste
        #    Usamos o PaymentMethod ID especial do Stripe para teste: pm_card_visa
        payment_method, _ = PaymentMethod.objects.get_or_create(
            tenant=tenant,
            gateway="stripe",
            gateway_payment_method_id="pm_card_visa",
            defaults={
                "type": "card",
                "card_last4": "4242",
                "card_brand": "visa",
                "is_default": True,
                "billing_details": {"name": "Stripe Test User", "email": tenant.email},
            },
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Método de pagamento de teste criado/usado: {payment_method.gateway_payment_method_id}"
            )
        )

        # 4. Criar ou reutilizar assinatura para o tenant de teste
        if hasattr(tenant, "subscription"):
            subscription = tenant.subscription
            self.stdout.write(
                self.style.WARNING(
                    f"ℹ️  Reutilizando assinatura existente: {subscription.id} (status: {subscription.status})"
                )
            )
        else:
            subscription = BillingService.create_subscription(
                tenant=tenant,
                plan=plan,
                payment_method=payment_method,
                billing_cycle="monthly",
            )
            self.stdout.write(
                self.style.SUCCESS(f"✅ Assinatura criada: {subscription.id} (status: {subscription.status})")
            )

        # 5. Criar fatura de teste
        invoice = InvoiceService.generate_invoice(subscription)
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Fatura criada: {invoice.invoice_number} - {invoice.total_amount} {invoice.currency} (status: {invoice.status})"
            )
        )

        # 6. Processar pagamento via Stripe
        self.stdout.write(self.style.MIGRATE_HEADING("💳 Enviando pagamento de teste para o Stripe..."))
        payment = PaymentService.process_payment(invoice, payment_method)

        invoice.refresh_from_db()
        payment.refresh_from_db()

        self.stdout.write(self.style.SUCCESS(f"✅ Pagamento criado: {payment.id} (status: {payment.status})"))
        self.stdout.write(self.style.SUCCESS(f"   gateway_payment_id: {payment.gateway_payment_id}"))
        self.stdout.write(self.style.SUCCESS(f"   gateway_charge_id: {payment.gateway_charge_id or 'N/A'}"))

        if invoice.status == "paid":
            self.stdout.write(
                self.style.SUCCESS(
                    f"🎉 SUCESSO: Stripe respondeu OK. Fatura {invoice.invoice_number} marcada como paga."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️ Pagamento processado, mas fatura ainda está com status '{invoice.status}'. "
                    "Verifique os logs e o painel do Stripe (PaymentIntent)."
                )
            )


