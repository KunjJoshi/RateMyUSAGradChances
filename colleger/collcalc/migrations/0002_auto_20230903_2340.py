# Generated by Django 3.2 on 2023-09-03 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collcalc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
