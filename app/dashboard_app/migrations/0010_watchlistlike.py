# Generated by Django 4.1.3 on 2023-07-13 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard_app', '0009_watchlist_price_change'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchlistLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard_app.watchlist')),
            ],
        ),
    ]