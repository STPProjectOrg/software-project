# Generated by Django 4.1.3 on 2023-05-30 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings_app', '0006_alter_settings_assetamountchanged'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='assetAmountChanged',
            field=models.BooleanField(default=None),
        ),
    ]
