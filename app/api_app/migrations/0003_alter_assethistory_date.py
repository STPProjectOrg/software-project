# Generated by Django 4.1.3 on 2023-05-04 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0002_alter_assethistory_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assethistory',
            name='date',
            field=models.DateField(),
        ),
    ]
