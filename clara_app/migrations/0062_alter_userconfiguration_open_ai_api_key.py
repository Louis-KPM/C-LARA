# Generated by Django 4.2.1 on 2024-03-08 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0061_userconfiguration_open_ai_api_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconfiguration',
            name='open_ai_api_key',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
