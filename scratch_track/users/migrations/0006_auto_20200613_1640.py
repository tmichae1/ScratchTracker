# Generated by Django 3.0.5 on 2020-06-13 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200613_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_id',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
    ]
