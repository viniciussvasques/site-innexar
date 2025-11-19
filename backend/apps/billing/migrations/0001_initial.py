# Generated migration - Billing Models

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenants', '0003_fix_subscription_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Nome do plano (ex: "Básico", "Profissional", "Starter")', max_length=100, verbose_name='Nome')),
                ('slug', models.SlugField(help_text='Identificador único do plano (ex: "basic", "professional")', unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('price_monthly_brl', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Preço Mensal (BRL)')),
                ('price_yearly_brl', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Preço Anual (BRL)')),
                ('price_monthly_usd', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Preço Mensal (USD)')),
                ('price_yearly_usd', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Preço Anual (USD)')),
                ('currency', models.CharField(choices=[('BRL', 'Real Brasileiro'), ('USD', 'Dólar Americano'), ('EUR', 'Euro')], default='BRL', max_length=3, verbose_name='Moeda Padrão')),
                ('max_projects', models.IntegerField(default=1, help_text='Número máximo de projetos permitidos (0 = ilimitado)', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Máximo de Projetos')),
                ('max_users', models.IntegerField(default=1, help_text='Número máximo de usuários permitidos (0 = ilimitado)', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Máximo de Usuários')),
                ('max_storage_gb', models.IntegerField(default=1, help_text='Armazenamento máximo em GB (0 = ilimitado)', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Armazenamento (GB)')),
                ('features', models.JSONField(default=list, help_text='Lista de features do plano (ex: ["Relatórios", "API", "Suporte 24/7"])', verbose_name='Features')),
                ('is_active', models.BooleanField(default=True, help_text='Se o plano está ativo e disponível para assinatura', verbose_name='Ativo')),
                ('is_featured', models.BooleanField(default=False, help_text='Se o plano deve ser destacado na página de planos', verbose_name='Destaque')),
                ('trial_days', models.IntegerField(default=0, help_text='Número de dias de trial grátis (0 = sem trial)', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Dias de Trial')),
                ('display_order', models.IntegerField(default=0, verbose_name='Ordem de Exibição')),
            ],
            options={
                'verbose_name': 'Plano',
                'verbose_name_plural': 'Planos',
                'ordering': ['display_order', 'price_monthly_brl'],
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('card', 'Cartão de Crédito'), ('boleto', 'Boleto Bancário'), ('pix', 'PIX')], default='card', max_length=20, verbose_name='Tipo')),
                ('gateway', models.CharField(choices=[('asaas', 'Asaas'), ('stripe', 'Stripe')], default='asaas', max_length=20, verbose_name='Gateway')),
                ('gateway_payment_method_id', models.CharField(max_length=255, unique=True, verbose_name='ID do Método no Gateway')),
                ('is_default', models.BooleanField(default=False, verbose_name='Padrão')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('card_last4', models.CharField(blank=True, help_text='Últimos 4 dígitos do cartão (apenas para exibição)', max_length=4, null=True, verbose_name='Últimos 4 Dígitos')),
                ('card_brand', models.CharField(blank=True, choices=[('visa', 'Visa'), ('mastercard', 'Mastercard'), ('amex', 'American Express'), ('discover', 'Discover')], max_length=20, null=True, verbose_name='Bandeira')),
                ('card_exp_month', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Mês de Expiração')),
                ('card_exp_year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(2020)], verbose_name='Ano de Expiração')),
                ('billing_details', models.JSONField(default=dict, verbose_name='Detalhes de Cobrança')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', to='tenants.tenant', verbose_name='Tenant')),
            ],
            options={
                'verbose_name': 'Método de Pagamento',
                'verbose_name_plural': 'Métodos de Pagamento',
                'ordering': ['-is_default', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('trialing', 'Em Trial'), ('active', 'Ativa'), ('past_due', 'Pagamento Atrasado'), ('canceled', 'Cancelada'), ('unpaid', 'Não Paga')], default='trialing', max_length=20, verbose_name='Status')),
                ('current_period_start', models.DateField(verbose_name='Início do Período')),
                ('current_period_end', models.DateField(verbose_name='Fim do Período')),
                ('trial_start', models.DateField(blank=True, null=True, verbose_name='Início do Trial')),
                ('trial_end', models.DateField(blank=True, null=True, verbose_name='Fim do Trial')),
                ('cancel_at_period_end', models.BooleanField(default=False, verbose_name='Cancelar ao Fim do Período')),
                ('canceled_at', models.DateTimeField(blank=True, null=True, verbose_name='Cancelada em')),
                ('cancellation_reason', models.TextField(blank=True, verbose_name='Motivo do Cancelamento')),
                ('gateway', models.CharField(choices=[('asaas', 'Asaas'), ('stripe', 'Stripe')], default='asaas', max_length=20, verbose_name='Gateway')),
                ('gateway_subscription_id', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='ID da Assinatura no Gateway')),
                ('gateway_customer_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='ID do Cliente no Gateway')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscriptions', to='billing.paymentmethod', verbose_name='Método de Pagamento')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='billing.plan', verbose_name='Plano')),
                ('tenant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='tenants.tenant', verbose_name='Tenant')),
            ],
            options={
                'verbose_name': 'Assinatura',
                'verbose_name_plural': 'Assinaturas',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('invoice_number', models.CharField(max_length=50, unique=True, verbose_name='Número da Fatura')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Valor')),
                ('currency', models.CharField(choices=[('BRL', 'Real Brasileiro'), ('USD', 'Dólar Americano'), ('EUR', 'Euro')], default='BRL', max_length=3, verbose_name='Moeda')),
                ('tax_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Valor de Impostos')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Valor Total')),
                ('status', models.CharField(choices=[('draft', 'Rascunho'), ('open', 'Aberta'), ('paid', 'Paga'), ('void', 'Cancelada'), ('uncollectible', 'Inadimplente')], default='draft', max_length=20, verbose_name='Status')),
                ('issue_date', models.DateField(verbose_name='Data de Emissão')),
                ('due_date', models.DateField(verbose_name='Data de Vencimento')),
                ('paid_at', models.DateTimeField(blank=True, null=True, verbose_name='Paga em')),
                ('gateway_invoice_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='ID da Fatura no Gateway')),
                ('gateway_pdf_url', models.URLField(blank=True, null=True, verbose_name='URL do PDF')),
                ('line_items', models.JSONField(default=list, verbose_name='Itens da Fatura')),
                ('notes', models.TextField(blank=True, verbose_name='Observações')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='billing.subscription', verbose_name='Assinatura')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='tenants.tenant', verbose_name='Tenant')),
            ],
            options={
                'verbose_name': 'Fatura',
                'verbose_name_plural': 'Faturas',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Valor')),
                ('currency', models.CharField(choices=[('BRL', 'Real Brasileiro'), ('USD', 'Dólar Americano'), ('EUR', 'Euro')], default='BRL', max_length=3, verbose_name='Moeda')),
                ('status', models.CharField(choices=[('pending', 'Pendente'), ('processing', 'Processando'), ('succeeded', 'Sucesso'), ('failed', 'Falhou'), ('refunded', 'Reembolsado'), ('canceled', 'Cancelado')], default='pending', max_length=20, verbose_name='Status')),
                ('payment_method_type', models.CharField(choices=[('card', 'Cartão de Crédito'), ('boleto', 'Boleto Bancário'), ('pix', 'PIX'), ('bank_transfer', 'Transferência Bancária'), ('ach', 'ACH (Transferência Bancária)')], max_length=20, verbose_name='Tipo de Método')),
                ('gateway', models.CharField(choices=[('asaas', 'Asaas'), ('stripe', 'Stripe')], default='asaas', max_length=20, verbose_name='Gateway')),
                ('gateway_payment_id', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='ID do Pagamento no Gateway')),
                ('gateway_charge_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='ID da Cobrança no Gateway')),
                ('failure_reason', models.TextField(blank=True, null=True, verbose_name='Motivo da Falha')),
                ('retry_count', models.IntegerField(default=0, verbose_name='Tentativas')),
                ('max_retries', models.IntegerField(default=3, verbose_name='Máximo de Tentativas')),
                ('metadata', models.JSONField(default=dict, verbose_name='Metadados')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='billing.invoice', verbose_name='Fatura')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='billing.paymentmethod', verbose_name='Método de Pagamento')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='tenants.tenant', verbose_name='Tenant')),
            ],
            options={
                'verbose_name': 'Pagamento',
                'verbose_name_plural': 'Pagamentos',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='plan',
            index=models.Index(fields=['slug'], name='billing_pla_slug_idx'),
        ),
        migrations.AddIndex(
            model_name='plan',
            index=models.Index(fields=['is_active'], name='billing_pla_is_acti_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['tenant'], name='billing_sub_tenant_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['status'], name='billing_sub_status_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['current_period_end'], name='billing_sub_current_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['tenant'], name='billing_invo_tenant_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['status'], name='billing_invo_status_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['due_date'], name='billing_invo_due_dat_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['invoice_number'], name='billing_invo_invoice_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['invoice'], name='billing_paym_invoice_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['tenant'], name='billing_payment_tenant_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['status'], name='billing_paym_status_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['gateway_payment_id'], name='billing_paym_gateway_idx'),
        ),
        migrations.AddIndex(
            model_name='paymentmethod',
            index=models.Index(fields=['tenant'], name='billing_paym_tenant_idx'),
        ),
        migrations.AddIndex(
            model_name='paymentmethod',
            index=models.Index(fields=['is_default'], name='billing_paym_is_defa_idx'),
        ),
    ]

