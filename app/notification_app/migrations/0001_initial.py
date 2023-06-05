# Generated by Django 4.1.3 on 2023-06-04 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('FOLLOWER', 'Wenn jemand ihnen folgt'), ('COMMENT', 'Wenn jemand ihren Beitrag kommentiert'), ('LIKE_POST', 'Wenn jemand ihren Beitrag liked'), ('LIKE_COMMENT', 'Wenn jemand ihren Kommentar liked'), ('COMMENT_ON_COMMENT', 'Wenn jemand ihren Kommentar kommentiert'), ('SHARE_POST', 'Wenn jemand ihren Beitrag teilt')], max_length=20)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]