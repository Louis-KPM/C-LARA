# Generated by Django 4.2.1 on 2024-01-24 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0044_alter_claraproject_l1_alter_claraproject_l2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='formatpreferences',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='formatpreferences',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='humanaudioinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='humanaudioinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='phonetichumanaudioinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='phonetichumanaudioinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
