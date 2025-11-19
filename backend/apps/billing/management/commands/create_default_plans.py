"""
Management command to create or update default billing plans.
Cria planos pensados para construtoras/incorporadoras, em BRL e USD,
com foco em conversão (free → basic → professional → enterprise).
"""
from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.billing.models import Plan


class Command(BaseCommand):
    help = "Cria ou atualiza os planos padrão de billing"

    def handle(self, *args, **options):
        plans_data = [
            {
                # Plano de entrada / teste
                "name": "Free / Teste",
                "slug": "free",
                "description": (
                    "Plano gratuito para testar o StructurOne em projetos pequenos. "
                    "Ideal para freelancers e micro construtoras."
                ),
                "price_monthly_brl": Decimal("0.00"),
                "price_yearly_brl": Decimal("0.00"),
                "price_monthly_usd": Decimal("0.00"),
                "price_yearly_usd": Decimal("0.00"),
                "currency": "BRL",
                "max_projects": 1,
                "max_users": 1,
                "max_storage_gb": 1,
                "features": [
                    "1 projeto ativo",
                    "1 usuário",
                    "Dashboard básico",
                    "Onboarding guiado",
                ],
                "trial_days": 0,
                "is_active": True,
                "is_featured": False,
                "display_order": 0,
            },
            {
                # Pequenas construtoras – foco BR
                "name": "Essencial",
                "slug": "essential",
                "description": (
                    "Para pequenas construtoras que querem sair do Excel e centralizar "
                    "obras, clientes e investidores em um só lugar."
                ),
                "price_monthly_brl": Decimal("197.00"),
                "price_yearly_brl": Decimal("1970.00"),
                "price_monthly_usd": Decimal("39.00"),
                "price_yearly_usd": Decimal("390.00"),
                "currency": "BRL",
                "max_projects": 3,
                "max_users": 3,
                "max_storage_gb": 5,
                "features": [
                    "Até 3 projetos ativos",
                    "Até 3 usuários",
                    "Dashboard financeiro básico",
                    "Controle simples de investidores",
                    "Relatórios PDF padrão",
                    "Suporte por email",
                ],
                "trial_days": 7,
                "is_active": True,
                "is_featured": False,
                "display_order": 1,
            },
            {
                # Plano que já definimos como base
                "name": "Profissional",
                "slug": "professional",
                "description": (
                    "Plano ideal para construtoras e incorporadoras em crescimento, "
                    "com múltiplos empreendimentos e equipe dedicada."
                ),
                "price_monthly_brl": Decimal("797.00"),
                "price_yearly_brl": Decimal("7970.00"),
                "price_monthly_usd": Decimal("99.00"),
                "price_yearly_usd": Decimal("990.00"),
                "currency": "BRL",
                "max_projects": 20,
                "max_users": 20,
                "max_storage_gb": 50,
                "features": [
                    "Até 20 projetos ativos",
                    "Até 20 usuários",
                    "Dashboard avançado (projetos, vendas, captação)",
                    "Módulo de investidores",
                    "Fluxos de aprovação",
                    "Exportação avançada (CSV / Excel)",
                    "Suporte prioritário em horário comercial",
                ],
                "trial_days": 14,
                "is_active": True,
                "is_featured": True,  # Plano de destaque
                "display_order": 2,
            },
            {
                # Plano foco internacional / empresas maiores
                "name": "Enterprise",
                "slug": "enterprise",
                "description": (
                    "Para grupos econômicos, holdings e incorporadoras com alto volume "
                    "de projetos, múltiplos CNPJs e times grandes."
                ),
                "price_monthly_brl": Decimal("1997.00"),
                "price_yearly_brl": Decimal("19970.00"),
                "price_monthly_usd": Decimal("349.00"),
                "price_yearly_usd": Decimal("3490.00"),
                "currency": "BRL",
                "max_projects": 0,  # 0 = ilimitado
                "max_users": 0,
                "max_storage_gb": 0,
                "features": [
                    "Projetos ilimitados",
                    "Usuários ilimitados",
                    "Múltiplos CNPJs / tenants",
                    "Relatórios customizados",
                    "Integrações avançadas (API, ERP, CRM)",
                    "Suporte dedicado e SLA",
                    "Onboarding personalizado",
                ],
                "trial_days": 0,  # Enterprise normalmente sem trial aberto
                "is_active": True,
                "is_featured": False,
                "display_order": 3,
            },
        ]

        created = 0
        updated = 0

        for data in plans_data:
            slug = data["slug"]
            defaults = {k: v for k, v in data.items() if k != "slug"}
            obj, is_created = Plan.objects.update_or_create(slug=slug, defaults=defaults)
            if is_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Plano criado: {obj.name} ({obj.slug})"))
            else:
                updated += 1
                self.stdout.write(self.style.WARNING(f"Plano atualizado: {obj.name} ({obj.slug})"))

        self.stdout.write(
            self.style.SUCCESS(f"Concluído. Planos criados: {created}, atualizados: {updated}.")
        )


