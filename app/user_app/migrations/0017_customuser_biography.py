# Generated by Django 4.1.3 on 2023-08-01 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0016_alter_profilebanner_profile_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='biography',
            field=models.TextField(blank=True),
        ),
    ]
