# Generated by Django 3.2 on 2023-09-04 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collcalc', '0003_universities_world_ranking'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='backlogs_in_first_two_sems',
            field=models.CharField(blank=True, default='0', max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='backlogs_in_rest',
            field=models.CharField(blank=True, default='0', max_length=3, null=True),
        ),
    ]
