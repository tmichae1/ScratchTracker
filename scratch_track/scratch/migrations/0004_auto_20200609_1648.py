# Generated by Django 3.0.7 on 2020-06-09 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scratch', '0003_auto_20200607_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scratch',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='scratch',
            name='time',
            field=models.TimeField(),
        ),
    ]
