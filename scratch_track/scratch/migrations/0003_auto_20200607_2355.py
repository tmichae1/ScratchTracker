# Generated by Django 3.0.7 on 2020-06-07 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scratch', '0002_auto_20200607_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scratch',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='scratch',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
