# Generated by Django 4.2 on 2023-06-11 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0005_transaction_charge_transaction_cost_transaction_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='price',
            field=models.FloatField(default=13),
            preserve_default=False,
        ),
    ]
