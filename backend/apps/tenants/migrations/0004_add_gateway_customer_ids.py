from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0003_fix_subscription_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='asaas_customer_id',
            field=models.CharField(
                blank=True,
                help_text='Identificador do cliente no Asaas',
                max_length=255,
                null=True,
                verbose_name='Asaas Customer ID',
            ),
        ),
        migrations.AddField(
            model_name='tenant',
            name='stripe_customer_id',
            field=models.CharField(
                blank=True,
                help_text='Identificador do cliente no Stripe',
                max_length=255,
                null=True,
                verbose_name='Stripe Customer ID',
            ),
        ),
    ]


