"""
Billing Views
ViewSets e endpoints para planos, assinaturas, faturas e pagamentos
"""
import logging

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from .models import Plan, Subscription, Invoice, Payment, PaymentMethod
from .serializers import (
    PlanSerializer,
    SubscriptionSerializer,
    InvoiceSerializer,
    PaymentSerializer,
    PaymentMethodSerializer,
    CreateSubscriptionSerializer,
    UpgradeSubscriptionSerializer,
    CancelSubscriptionSerializer,
    CreatePaymentMethodSerializer,
)
from .services import BillingService, InvoiceService, PaymentService
from .gateway.stripe import StripeGatewayService
from apps.core.permissions import IsTenantOwner
from apps.core.models import User

logger = logging.getLogger(__name__)


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão para billing"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Planos
    Apenas leitura - criação/edição via admin
    """
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    pagination_class = None  # Planos são poucos, não precisa paginação
    
    def get_queryset(self):
        """Filtrar planos ativos"""
        return Plan.objects.filter(is_active=True).order_by('display_order', 'price_monthly_brl')
    
    def get_serializer_context(self):
        """Adicionar request ao contexto do serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Assinaturas
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantOwner]
    
    def get_queryset(self):
        """Retornar apenas assinatura do tenant do usuário"""
        user = self.request.user
        if isinstance(user, User) and hasattr(user, 'tenant') and user.tenant:
            return Subscription.objects.filter(tenant=user.tenant)
        return Subscription.objects.none()
    
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Retorna assinatura atual do tenant"""
        user = request.user
        if not isinstance(user, User) or not hasattr(user, 'tenant') or not user.tenant:
            return Response(
                {'detail': 'Usuário não possui tenant'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            subscription = Subscription.objects.get(tenant=user.tenant)
            serializer = self.get_serializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response(
                {'detail': 'Nenhuma assinatura encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'], url_path='create')
    def create_subscription(self, request):
        """Cria nova assinatura"""
        serializer = CreateSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not isinstance(user, User) or not hasattr(user, 'tenant') or not user.tenant:
            return Response(
                {'detail': 'Usuário não possui tenant'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plan = serializer.validated_data['plan_id']
        payment_method = serializer.validated_data.get('payment_method_id')
        billing_cycle = serializer.validated_data.get('billing_cycle', 'monthly')
        
        try:
            subscription = BillingService.create_subscription(
                tenant=user.tenant,
                plan=plan,
                payment_method=payment_method,
                billing_cycle=billing_cycle
            )
            
            # Gerar primeira fatura
            invoice = InvoiceService.generate_invoice(subscription)
            
            # Processar pagamento se método disponível
            if payment_method:
                PaymentService.process_payment(invoice, payment_method)
            
            response_serializer = SubscriptionSerializer(subscription)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['patch'], url_path='upgrade')
    def upgrade(self, request, pk=None):
        """Faz upgrade de assinatura"""
        subscription = self.get_object()
        serializer = UpgradeSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_plan = serializer.validated_data['plan_id']
        
        try:
            subscription, adjustment_invoice = BillingService.upgrade_subscription(
                subscription, new_plan
            )
            
            response_serializer = SubscriptionSerializer(subscription)
            response_data = response_serializer.data
            
            if adjustment_invoice:
                response_data['adjustment_invoice'] = InvoiceSerializer(adjustment_invoice).data
            
            return Response(response_data)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['patch'], url_path='cancel')
    def cancel(self, request, pk=None):
        """Cancela assinatura"""
        subscription = self.get_object()
        serializer = CancelSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reason = serializer.validated_data.get('reason', '')
        
        try:
            subscription = BillingService.cancel_subscription(subscription, reason)
            response_serializer = SubscriptionSerializer(subscription)
            return Response(response_serializer.data)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Faturas
    Apenas leitura - criação automática pelo sistema
    """
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantOwner]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Retornar apenas faturas do tenant do usuário"""
        user = self.request.user
        if isinstance(user, User) and hasattr(user, 'tenant') and user.tenant:
            queryset = Invoice.objects.filter(tenant=user.tenant).select_related(
                'subscription', 'subscription__plan'
            ).order_by('-created_at')
            
            # Filtros opcionais
            status_filter = self.request.query_params.get('status', None)
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            return queryset
        return Invoice.objects.none()

    @action(detail=True, methods=["post"], url_path="pay")
    def pay(self, request, pk=None):
        """
        Processa pagamento de uma fatura
        - Usa payment_method_id enviado no body OU o método padrão do tenant
        """
        invoice = self.get_object()
        user = request.user

        # Garantir que o usuário pertence ao tenant da fatura
        if not isinstance(user, User) or not hasattr(user, "tenant") or user.tenant != invoice.tenant:
            return Response(
                {"detail": "Você não tem permissão para pagar esta fatura."},
                status=status.HTTP_403_FORBIDDEN,
            )

        payment_method_id = request.data.get("payment_method_id")
        payment_method = None

        if payment_method_id:
            payment_method = get_object_or_404(
                PaymentMethod, id=payment_method_id, tenant=invoice.tenant
            )

        try:
            payment = PaymentService.process_payment(invoice, payment_method)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro ao processar pagamento da fatura {invoice.id}: {e}")
            return Response(
                {"detail": "Erro ao processar pagamento da fatura."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=['get'], url_path='pdf')
    def pdf(self, request, pk=None):
        """Download do PDF da fatura"""
        invoice = self.get_object()
        
        if invoice.gateway_pdf_url:
            return Response({'pdf_url': invoice.gateway_pdf_url})
        
        return Response(
            {'detail': 'PDF não disponível'},
            status=status.HTTP_404_NOT_FOUND
        )


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Pagamentos
    Apenas leitura - criação automática pelo sistema
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantOwner]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Retornar apenas pagamentos do tenant do usuário"""
        user = self.request.user
        if isinstance(user, User) and hasattr(user, 'tenant') and user.tenant:
            queryset = Payment.objects.filter(tenant=user.tenant).select_related(
                'invoice', 'payment_method'
            ).order_by('-created_at')
            
            # Filtros opcionais
            status_filter = self.request.query_params.get('status', None)
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            return queryset
        return Payment.objects.none()


class PaymentMethodViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Métodos de Pagamento
    """
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantOwner]
    
    def get_queryset(self):
        """Retornar apenas métodos de pagamento do tenant do usuário"""
        user = self.request.user
        if isinstance(user, User) and hasattr(user, 'tenant') and user.tenant:
            return PaymentMethod.objects.filter(tenant=user.tenant).order_by('-is_default', '-created_at')
        return PaymentMethod.objects.none()

    def create(self, request, *args, **kwargs):
        """Cria método de pagamento com tokenização"""
        user = request.user
        if not isinstance(user, User) or not hasattr(user, 'tenant') or not user.tenant:
            return Response(
                {'detail': 'Usuário não possui tenant configurado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tenant = user.tenant

        data_serializer = CreatePaymentMethodSerializer(data=request.data)
        data_serializer.is_valid(raise_exception=True)
        validated = data_serializer.validated_data

        payment_type = validated['type']
        token = validated['token']
        is_default = validated.get('is_default', False)
        billing_details = validated.get('billing_details', {}) or {}

        if payment_type != 'card':
            return Response(
                {'detail': 'Apenas cartões de crédito são suportados no momento.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Enquanto a captura de cartões via Asaas está em desenvolvimento, usamos Stripe
        gateway = 'stripe' if tenant.country != 'BR' else 'stripe'
        if gateway != 'stripe':
            return Response(
                {'detail': 'Integração de cartão para este país ainda não está disponível.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        gateway_service = StripeGatewayService()

        # Garantir customer no Stripe
        customer_id = tenant.stripe_customer_id
        if not customer_id:
            try:
                customer_id = gateway_service.create_customer(tenant)
                tenant.stripe_customer_id = customer_id
                tenant.save(update_fields=['stripe_customer_id'])
            except Exception as exc:
                logger.error('Erro ao criar cliente no Stripe: %s', exc)
                return Response(
                    {'detail': 'Não foi possível criar o cliente no Stripe.'},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

        try:
            payment_method_info = gateway_service.create_payment_method(token, customer_id)
        except Exception as exc:
            logger.error('Erro ao anexar método de pagamento no Stripe: %s', exc)
            return Response(
                {'detail': 'Não foi possível validar o cartão informado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        gateway_payment_method_id = payment_method_info.get('id')
        if not gateway_payment_method_id:
            return Response(
                {'detail': 'Stripe não retornou identificador do método de pagamento.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        card_info = payment_method_info.get('card') or {}
        brand = (card_info.get('brand') or '').lower()
        brand_map = {
            'american express': 'amex',
            'amex': 'amex',
            'visa': 'visa',
            'mastercard': 'mastercard',
            'discover': 'discover',
            'diners': 'mastercard',  # fallback
        }
        normalized_brand = brand_map.get(brand, brand)
        if normalized_brand not in dict(PaymentMethod._meta.get_field('card_brand').choices).keys():
            normalized_brand = None

        should_be_default = is_default or not PaymentMethod.objects.filter(tenant=tenant).exists()
        if should_be_default:
            PaymentMethod.objects.filter(tenant=tenant, is_default=True).update(is_default=False)

        payment_method = PaymentMethod.objects.create(
            tenant=tenant,
            type=payment_type,
            gateway=gateway,
            gateway_payment_method_id=gateway_payment_method_id,
            is_default=should_be_default,
            billing_details=billing_details,
            card_last4=card_info.get('last4'),
            card_brand=normalized_brand,
            card_exp_month=card_info.get('exp_month'),
            card_exp_year=card_info.get('exp_year'),
        )

        # Atualizar assinatura existente para usar o novo método
        subscription = getattr(tenant, 'subscription', None)
        if subscription:
            update_fields = []
            if subscription.payment_method_id != payment_method.id:
                subscription.payment_method = payment_method
                update_fields.append('payment_method')

            if subscription.gateway != gateway:
                subscription.gateway = gateway
                update_fields.append('gateway')

            if gateway == 'stripe' and tenant.stripe_customer_id:
                if subscription.gateway_customer_id != tenant.stripe_customer_id:
                    subscription.gateway_customer_id = tenant.stripe_customer_id
                    update_fields.append('gateway_customer_id')
            elif gateway == 'asaas' and tenant.asaas_customer_id:
                if subscription.gateway_customer_id != tenant.asaas_customer_id:
                    subscription.gateway_customer_id = tenant.asaas_customer_id
                    update_fields.append('gateway_customer_id')

            if update_fields:
                subscription.save(update_fields=update_fields)

        serializer = self.get_serializer(payment_method)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'], url_path='set-default')
    def set_default(self, request, pk=None):
        """Define método de pagamento como padrão"""
        payment_method = self.get_object()
        
        # Remover padrão de outros métodos
        PaymentMethod.objects.filter(
            tenant=payment_method.tenant,
            is_default=True
        ).update(is_default=False)
        
        # Definir este como padrão
        payment_method.is_default = True
        payment_method.save()
        
        serializer = self.get_serializer(payment_method)
        return Response(serializer.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def stripe_webhook(request):
    """
    Webhook do Stripe
    - Valida assinatura usando STRIPE_WEBHOOK_SECRET
    - Atualiza pagamentos/faturas quando receber payment_intent.succeeded
    """
    gateway = StripeGatewayService()
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        result = gateway.handle_webhook(request.body, sig_header)
    except Exception as e:
        logger.error(f"Erro ao validar webhook do Stripe: {e}")
        return Response({"detail": "Payload inválido"}, status=status.HTTP_400_BAD_REQUEST)

    event = result.get("event")
    payment_id = result.get("payment_id")
    data = result.get("data", {})

    logger.info(f"Webhook Stripe recebido: {event} - {payment_id}")

    if event == "payment_intent.succeeded" and payment_id:
        # Tenta localizar pagamento pelo gateway_payment_id
        payment = Payment.objects.filter(gateway_payment_id=payment_id).first()

        # Fallback: tentar via invoice_number em metadata
        if not payment:
            metadata = data.get("metadata", {}) if isinstance(data, dict) else {}
            invoice_number = metadata.get("invoice_id") or metadata.get("invoice_number")
            if invoice_number:
                invoice = Invoice.objects.filter(invoice_number=invoice_number).first()
                if invoice:
                    payment = invoice.payments.order_by("-created_at").first()

        if payment:
            PaymentService.mark_payment_succeeded(payment, gateway_payment_id=payment_id)
        else:
            logger.warning(
                f"Webhook Stripe payment_intent.succeeded sem Payment associado. payment_id={payment_id}"
            )

    # Outros eventos podem ser tratados no futuro (falha, cancelamento etc.)

    return Response({"status": "ok"})

