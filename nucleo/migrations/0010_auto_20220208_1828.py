# Generated by Django 3.1.2 on 2022-02-08 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0009_auto_20220208_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyect',
            name='endDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proyect',
            name='endingReport',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]