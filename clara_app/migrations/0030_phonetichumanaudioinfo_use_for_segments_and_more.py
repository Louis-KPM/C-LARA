# Generated by Django 4.2.1 on 2023-11-29 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0029_remove_phonetichumanaudioinfo_use_for_segments_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonetichumanaudioinfo',
            name='use_for_segments',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='phonetichumanaudioinfo',
            name='use_for_words',
            field=models.BooleanField(default=True),
        ),
    ]