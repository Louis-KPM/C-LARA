# Generated by Django 4.2.1 on 2024-01-14 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0040_phonetichumanaudioinfo_preferred_tts_engine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='humanaudioinfo',
            name='method',
            field=models.CharField(choices=[('tts_only', 'TTS only'), ('upload', 'Upload'), ('record', 'Record'), ('manual_align', 'Manual Align'), ('automatic_align', 'Automatic Align')], max_length=20),
        ),
    ]
