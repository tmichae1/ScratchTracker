# Generated by Django 3.0.5 on 2020-06-18 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scratch', '0009_nightscratch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nightscratch',
            name='points',
            field=models.IntegerField(),
        ),
    ]