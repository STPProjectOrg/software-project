# Generated by Django 4.1.3 on 2023-06-22 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_app', '0003_alter_assethistory_date'),
        ('dashboard_app', '0006_transaction_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addet_at', models.DateTimeField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.asset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
