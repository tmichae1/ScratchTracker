# Generated by Django 3.0.5 on 2020-07-29 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scratch', '0010_auto_20200618_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyscratchcount',
            name='date',
            field=models.DateField(),
        ),
    ]
