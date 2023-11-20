# Generated by Django 4.2.1 on 2023-11-17 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0025_userconfiguration_max_annotation_words'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claraproject',
            name='l1',
            field=models.CharField(choices=[('arabic', 'Arabic'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('mandarin', 'Mandarin'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese')], max_length=50),
        ),
        migrations.AlterField(
            model_name='claraproject',
            name='l2',
            field=models.CharField(choices=[('arabic', 'Arabic'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('mandarin', 'Mandarin'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese')], max_length=50),
        ),
        migrations.AlterField(
            model_name='languagemaster',
            name='language',
            field=models.CharField(choices=[('default', 'Default'), ('arabic', 'Arabic'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('mandarin', 'Mandarin'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese')], max_length=50),
        ),
    ]
