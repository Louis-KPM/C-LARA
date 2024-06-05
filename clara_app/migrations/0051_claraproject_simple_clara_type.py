# Generated by Django 4.2.1 on 2024-02-10 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0050_readinghistory_require_phonetic_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='claraproject',
            name='simple_clara_type',
            field=models.CharField(choices=[('create_text_and_image', 'Use the AI to create text and an image based on your instructions'), ('create_text_from_image', 'Upload an image and use the AI to create text from it'), ('annotate_existing_text', 'Paste in your own text and use the AI to convert it to multimodal form')], default='create_text_and_image', max_length=50),
        ),
    ]