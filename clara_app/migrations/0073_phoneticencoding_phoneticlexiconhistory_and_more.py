# Generated by Django 4.2.1 on 2024-04-05 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0072_imagemetadata_imagemetadata_unique_project_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneticEncoding',
            fields=[
                ('language', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('encoding', models.CharField(choices=[('ipa', 'IPA'), ('arpabet_like', 'Arpabet-like')], max_length=255)),
            ],
        ),
##        migrations.CreateModel(
##            name='PhoneticLexiconHistory',
##            fields=[
##                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
##                ('word', models.TextField()),
##                ('modification_date', models.DateTimeField()),
##                ('previous_value', models.JSONField()),
##                ('new_value', models.JSONField()),
##                ('modified_by', models.CharField(max_length=255)),
##                ('comments', models.TextField()),
##            ],
##            options={
##                'indexes': [models.Index(fields=['word'], name='idx_word_history')],
##            },
##        ),
        migrations.CreateModel(
            name='PlainPhoneticLexicon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('phonemes', models.TextField()),
                ('status', models.CharField(choices=[('uploaded', 'Uploaded'), ('generated', 'Generated'), ('reviewed', 'Reviewed')], max_length=255)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clara_app.phoneticencoding')),
            ],
##            options={
##                'indexes': [models.Index(fields=['word'], name='idx_word_plain')],
##            },
        ),
        migrations.CreateModel(
            name='AlignedPhoneticLexicon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('phonemes', models.TextField()),
                ('aligned_graphemes', models.TextField()),
                ('aligned_phonemes', models.TextField()),
                ('status', models.CharField(choices=[('uploaded', 'Uploaded'), ('generated', 'Generated'), ('reviewed', 'Reviewed')], max_length=255)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clara_app.phoneticencoding')),
            ],
##            options={
##                'indexes': [models.Index(fields=['word'], name='idx_word_aligned')],
##            },
        ),
    ]
