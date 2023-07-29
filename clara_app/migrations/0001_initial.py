# Generated by Django 4.2.1 on 2023-05-09 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('l2', models.CharField(max_length=100, verbose_name='L2 Language')),
                ('l1', models.CharField(max_length=100, verbose_name='L1 Language')),
                ('length_in_words', models.IntegerField()),
                ('author', models.CharField(max_length=255)),
                ('voice', models.CharField(max_length=255)),
                ('annotator', models.CharField(max_length=255)),
                ('difficulty_level', models.CharField(max_length=100)),
            ],
        ),
    ]
