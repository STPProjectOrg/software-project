# Generated by Django 4.1.3 on 2023-05-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_app', '0014_commentlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, upload_to='comment_images/'),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_images/'),
        ),
    ]
