# Generated by Django 3.0.5 on 2020-06-29 13:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20200629_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreport',
            name='antihistamine_120mg',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(0)]),
        ),
    ]
