# Generated by Django 4.1.3 on 2023-05-29 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_app', '0002_remove_postlikes_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
