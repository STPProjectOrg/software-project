# Generated by Django 4.1.3 on 2023-07-20 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0014_profilebanner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='profile_banner',
        ),
    ]
