# Generated by Django 4.1.3 on 2023-07-18 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0011_customuser_ws_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='ws_state',
        ),
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='biography',
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='profile_banner',
            field=models.CharField(choices=[('/static/banner_1.png', 'Banner 1'), ('/static/banner_2.png', 'Banner 2')], default='/static/banner_1.png', max_length=255),
        ),
    ]