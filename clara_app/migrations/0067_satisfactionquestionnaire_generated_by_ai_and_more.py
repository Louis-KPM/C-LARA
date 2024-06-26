# Generated by Django 4.2.1 on 2024-03-19 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clara_app', '0066_remove_satisfactionquestionnaire_cultural_appropriateness_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='satisfactionquestionnaire',
            name='generated_by_ai',
            field=models.BooleanField(default=True, verbose_name='Was your text originally generated by C-LARA or another AI?'),
        ),
        migrations.AlterField(
            model_name='satisfactionquestionnaire',
            name='content_appropriateness',
            field=models.IntegerField(choices=[(0, 'NOT APPLICABLE'), (5, 'Strongly agree'), (4, 'Agree'), (3, 'Neutral or not applicable'), (2, 'Disagree'), (1, 'Strongly disagree')], null=True, verbose_name='The overall content was appropriate'),
        ),
        migrations.AlterField(
            model_name='satisfactionquestionnaire',
            name='cultural_elements',
            field=models.IntegerField(choices=[(0, 'NOT APPLICABLE'), (5, 'Strongly agree'), (4, 'Agree'), (3, 'Neutral or not applicable'), (2, 'Disagree'), (1, 'Strongly disagree')], null=True, verbose_name='The text included appropriate elements of local culture'),
        ),
        migrations.AlterField(
            model_name='satisfactionquestionnaire',
            name='grammar_correctness',
            field=models.IntegerField(choices=[(0, 'NOT APPLICABLE'), (5, 'Strongly agree'), (4, 'Agree'), (3, 'Neutral or not applicable'), (2, 'Disagree'), (1, 'Strongly disagree')], null=True, verbose_name='The grammar in the text was correct'),
        ),
        migrations.AlterField(
            model_name='satisfactionquestionnaire',
            name='image_match',
            field=models.IntegerField(choices=[(0, 'NOT APPLICABLE'), (5, 'Strongly agree'), (4, 'Agree'), (3, 'Neutral or not applicable'), (2, 'Disagree'), (1, 'Strongly disagree')], null=True, verbose_name='The image(s) matched the content of the text'),
        ),
        migrations.AlterField(
            model_name='satisfactionquestionnaire',
            name='style_appropriateness',
            field=models.IntegerField(choices=[(0, 'NOT APPLICABLE'), (5, 'Strongly agree'), (4, 'Agree'), (3, 'Neutral or not applicable'), (2, 'Disagree'), (1, 'Strongly disagree')], null=True, verbose_name='The style was appropriate'),
        ),
        migrations.AlterField(
            model_name='satisfactionquestionnaire',
            name='text_engagement',
            field=models.IntegerField(choices=[(0, 'NOT APPLICABLE'), (5, 'Strongly agree'), (4, 'Agree'), (3, 'Neutral or not applicable'), (2, 'Disagree'), (1, 'Strongly disagree')], null=True, verbose_name='I found the text engaging (funny/cute/moving/etc)'),
        ),
        migrations.AlterField(
            model_name='satisfactionquestionnaire',
            name='vocabulary_appropriateness',
            field=models.IntegerField(choices=[(0, 'NOT APPLICABLE'), (5, 'Strongly agree'), (4, 'Agree'), (3, 'Neutral or not applicable'), (2, 'Disagree'), (1, 'Strongly disagree')], null=True, verbose_name='The vocabulary/choice of words was appropriate'),
        ),
    ]
