# Generated by Django 4.2.1 on 2023-11-13 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0024_userconfiguration'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconfiguration',
            name='max_annotation_words',
            field=models.IntegerField(default=100),
        ),
    ]
