# Generated by Django 4.1.3 on 2023-05-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging_app', '0004_alter_message_from_user_alter_message_to_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]