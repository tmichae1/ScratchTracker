# Generated by Django 3.0.5 on 2020-06-13 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_id',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
