# Generated by Django 4.2.1 on 2023-05-15 03:45

from django.db import migrations, models
import re

def generate_internal_id(apps, schema_editor):
    CLARAProject = apps.get_model('clara_app', 'CLARAProject')
    for project in CLARAProject.objects.all():
        project.internal_id = re.sub(r'\W+', '_', project.title) + str(project.id)
        project.save()

class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0002_claraproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='claraproject',
            name='internal_id',
            field=models.CharField(default='tmp', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='claraproject',
            name='l1',
            field=models.CharField(choices=[('arabic', 'Arabic'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('icelandic', 'Icelandic'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese')], max_length=50),
        ),
        migrations.AlterField(
            model_name='claraproject',
            name='l2',
            field=models.CharField(choices=[('arabic', 'Arabic'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('icelandic', 'Icelandic'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese')], max_length=50),
        ),
        migrations.RunPython(generate_internal_id),
    ]
