# Generated by Django 4.2.1 on 2024-04-07 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0071_alter_claraproject_l1_alter_claraproject_l2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneticEncoding',
            fields=[
                ('language', models.CharField(choices=[('american english', 'American English'), ('ancient egyptian', 'Ancient Egyptian'), ('arabic', 'Arabic'), ('australian english', 'Australian English'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('indonesian', 'Indonesian'), ('irish', 'Irish'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('malay', 'Malay'), ('mandarin', 'Mandarin'), ('māori', 'Māori'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('paicî', 'Paicî'), ('pitjantjatjara', 'Pitjantjatjara'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese'), ('welsh', 'Welsh'), ('west greenlandic', 'West Greenlandic')], max_length=255, primary_key=True, serialize=False)),
                ('encoding', models.CharField(choices=[('ipa', 'IPA'), ('arpabet_like', 'Arpabet-like')], max_length=255)),
            ],
            options={
                'db_table': 'orm_phonetic_encoding',
            },
        ),
        migrations.AlterField(
            model_name='claraproject',
            name='l1',
            field=models.CharField(choices=[('american english', 'American English'), ('ancient egyptian', 'Ancient Egyptian'), ('arabic', 'Arabic'), ('australian english', 'Australian English'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('indonesian', 'Indonesian'), ('irish', 'Irish'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('malay', 'Malay'), ('mandarin', 'Mandarin'), ('māori', 'Māori'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('paicî', 'Paicî'), ('pitjantjatjara', 'Pitjantjatjara'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese'), ('welsh', 'Welsh'), ('west greenlandic', 'West Greenlandic')], max_length=50),
        ),
        migrations.AlterField(
            model_name='claraproject',
            name='l2',
            field=models.CharField(choices=[('american english', 'American English'), ('ancient egyptian', 'Ancient Egyptian'), ('arabic', 'Arabic'), ('australian english', 'Australian English'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('indonesian', 'Indonesian'), ('irish', 'Irish'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('malay', 'Malay'), ('mandarin', 'Mandarin'), ('māori', 'Māori'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('paicî', 'Paicî'), ('pitjantjatjara', 'Pitjantjatjara'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese'), ('welsh', 'Welsh'), ('west greenlandic', 'West Greenlandic')], max_length=50),
        ),
        migrations.AlterField(
            model_name='fundingrequest',
            name='language',
            field=models.CharField(choices=[('american english', 'American English'), ('ancient egyptian', 'Ancient Egyptian'), ('arabic', 'Arabic'), ('australian english', 'Australian English'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('indonesian', 'Indonesian'), ('irish', 'Irish'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('malay', 'Malay'), ('mandarin', 'Mandarin'), ('māori', 'Māori'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('paicî', 'Paicî'), ('pitjantjatjara', 'Pitjantjatjara'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese'), ('welsh', 'Welsh'), ('west greenlandic', 'West Greenlandic'), ('other', 'Other')], max_length=50, verbose_name='In which language will you mostly be creating texts?'),
        ),
        migrations.AlterField(
            model_name='languagemaster',
            name='language',
            field=models.CharField(choices=[('default', 'Default'), ('american english', 'American English'), ('ancient egyptian', 'Ancient Egyptian'), ('arabic', 'Arabic'), ('australian english', 'Australian English'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('indonesian', 'Indonesian'), ('irish', 'Irish'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('malay', 'Malay'), ('mandarin', 'Mandarin'), ('māori', 'Māori'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('paicî', 'Paicî'), ('pitjantjatjara', 'Pitjantjatjara'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese'), ('welsh', 'Welsh'), ('west greenlandic', 'West Greenlandic')], max_length=50),
        ),
        migrations.AlterField(
            model_name='readinghistory',
            name='l2',
            field=models.CharField(choices=[('american english', 'American English'), ('ancient egyptian', 'Ancient Egyptian'), ('arabic', 'Arabic'), ('australian english', 'Australian English'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('indonesian', 'Indonesian'), ('irish', 'Irish'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('malay', 'Malay'), ('mandarin', 'Mandarin'), ('māori', 'Māori'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('paicî', 'Paicî'), ('pitjantjatjara', 'Pitjantjatjara'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese'), ('welsh', 'Welsh'), ('west greenlandic', 'West Greenlandic')], max_length=50),
        ),
        migrations.AlterModelTable(
            name='audiometadata',
            table='orm_audio_metadata',
        ),
        migrations.CreateModel(
            name='PlainPhoneticLexicon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('phonemes', models.TextField()),
                ('language', models.CharField(choices=[('american english', 'American English'), ('ancient egyptian', 'Ancient Egyptian'), ('arabic', 'Arabic'), ('australian english', 'Australian English'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('indonesian', 'Indonesian'), ('irish', 'Irish'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('malay', 'Malay'), ('mandarin', 'Mandarin'), ('māori', 'Māori'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('paicî', 'Paicî'), ('pitjantjatjara', 'Pitjantjatjara'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese'), ('welsh', 'Welsh'), ('west greenlandic', 'West Greenlandic')], max_length=255)),
                ('status', models.CharField(choices=[('uploaded', 'Uploaded'), ('generated', 'Generated'), ('reviewed', 'Reviewed')], max_length=255)),
            ],
            options={
                'db_table': 'orm_phonetic_lexicon',
                'indexes': [models.Index(fields=['word'], name='idx_word_plain')],
                'unique_together': {('language', 'word', 'phonemes')},
            },
        ),
        migrations.CreateModel(
            name='PhoneticLexiconHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('modification_date', models.DateTimeField()),
                ('previous_value', models.JSONField()),
                ('new_value', models.JSONField()),
                ('modified_by', models.CharField(max_length=255)),
                ('comments', models.TextField()),
            ],
            options={
                'db_table': 'orm_phonetic_lexicon_history',
                'indexes': [models.Index(fields=['word'], name='idx_word_history')],
            },
        ),
        migrations.CreateModel(
            name='ImageMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=255)),
                ('image_name', models.CharField(max_length=255)),
                ('file_path', models.TextField()),
                ('associated_text', models.TextField(blank=True, default='')),
                ('associated_areas', models.TextField(blank=True, default='')),
                ('page', models.IntegerField(default=1)),
                ('position', models.CharField(choices=[('top', 'Top'), ('bottom', 'Bottom'), ('inline', 'Inline')], default='top', max_length=10)),
            ],
            options={
                'verbose_name': 'Image Metadata',
                'verbose_name_plural': 'Image Metadata',
                'db_table': 'orm_image_metadata',
                'unique_together': {('project_id', 'image_name')},
            },
        ),
        migrations.CreateModel(
            name='AlignedPhoneticLexicon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('phonemes', models.TextField()),
                ('aligned_graphemes', models.TextField()),
                ('aligned_phonemes', models.TextField()),
                ('language', models.CharField(choices=[('american english', 'American English'), ('ancient egyptian', 'Ancient Egyptian'), ('arabic', 'Arabic'), ('australian english', 'Australian English'), ('barngarla', 'Barngarla'), ('bengali', 'Bengali'), ('bulgarian', 'Bulgarian'), ('cantonese', 'Cantonese'), ('chinese', 'Chinese'), ('croatian', 'Croatian'), ('czech', 'Czech'), ('danish', 'Danish'), ('drehu', 'Drehu'), ('dutch', 'Dutch'), ('english', 'English'), ('faroese', 'Faroese'), ('farsi', 'Farsi'), ('finnish', 'Finnish'), ('french', 'French'), ('german', 'German'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('hindi', 'Hindi'), ('hungarian', 'Hungarian'), ('iaai', 'Iaai'), ('icelandic', 'Icelandic'), ('indonesian', 'Indonesian'), ('irish', 'Irish'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('latin', 'Latin'), ('malay', 'Malay'), ('mandarin', 'Mandarin'), ('māori', 'Māori'), ('norwegian', 'Norwegian'), ('old norse', 'Old Norse'), ('paicî', 'Paicî'), ('pitjantjatjara', 'Pitjantjatjara'), ('polish', 'Polish'), ('portuguese', 'Portuguese'), ('romanian', 'Romanian'), ('russian', 'Russian'), ('serbian', 'Serbian'), ('slovak', 'Slovak'), ('slovenian', 'Slovenian'), ('spanish', 'Spanish'), ('swedish', 'Swedish'), ('thai', 'Thai'), ('turkish', 'Turkish'), ('ukrainian', 'Ukrainian'), ('vietnamese', 'Vietnamese'), ('welsh', 'Welsh'), ('west greenlandic', 'West Greenlandic')], max_length=255)),
                ('status', models.CharField(choices=[('uploaded', 'Uploaded'), ('generated', 'Generated'), ('reviewed', 'Reviewed')], max_length=255)),
            ],
            options={
                'db_table': 'orm_aligned_phonetic_lexicon',
                'indexes': [models.Index(fields=['word'], name='idx_word_aligned')],
                'unique_together': {('language', 'word', 'phonemes')},
            },
        ),
    ]
