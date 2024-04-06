# Generated by Django 4.2.1 on 2024-04-05 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0074_alter_alignedphoneticlexicon_language_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='imagemetadata',
            name='unique_project_image',
        ),
        migrations.AlterUniqueTogether(
            name='alignedphoneticlexicon',
            unique_together={('language', 'word', 'phonemes')},
        ),
        migrations.AlterUniqueTogether(
            name='audiometadata',
            unique_together={('engine_id', 'language_id', 'voice_id', 'text', 'context')},
        ),
        migrations.AlterUniqueTogether(
            name='imagemetadata',
            unique_together={('project_id', 'image_name')},
        ),
        migrations.AlterUniqueTogether(
            name='plainphoneticlexicon',
            unique_together={('language', 'word', 'phonemes')},
        ),
    ]
