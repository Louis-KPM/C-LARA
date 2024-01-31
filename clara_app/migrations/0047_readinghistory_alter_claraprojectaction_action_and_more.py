# Generated by Django 4.2.1 on 2024-01-31 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clara_app', '0046_content_created_at_content_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='claraprojectaction',
            name='action',
            field=models.CharField(choices=[('create', 'Create'), ('edit', 'Edit')], max_length=50),
        ),
        migrations.AlterField(
            model_name='claraprojectaction',
            name='text_version',
            field=models.CharField(choices=[('plain', 'Plain'), ('segmented', 'Segmented'), ('gloss', 'Gloss'), ('lemma', 'Lemma')], max_length=50),
        ),
        migrations.CreateModel(
            name='ReadingHistoryProjectOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clara_app.claraproject')),
                ('reading_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clara_app.readinghistory')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='readinghistory',
            name='projects',
            field=models.ManyToManyField(related_name='included_in_reading_histories', through='clara_app.ReadingHistoryProjectOrder', to='clara_app.claraproject'),
        ),
        migrations.AddField(
            model_name='readinghistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reading_histories', to=settings.AUTH_USER_MODEL),
        ),
    ]
