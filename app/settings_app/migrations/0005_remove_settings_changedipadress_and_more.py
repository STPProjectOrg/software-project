# Generated by Django 4.1.3 on 2023-05-30 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings_app', '0004_settings_assetamountchanged_settings_changedipadress_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='changedIpAdress',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='commentedMessage',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='followMessage',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='likedCommentMessage',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='likedPostMessage',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='sharedPostMessage',
        ),
    ]