# Generated by Django 3.0.5 on 2020-06-15 17:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('medication', '0002_delete_tabletandsteroid'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('nostril_used', models.CharField(blank=True, choices=[('left', 'Left'), ('right', 'Right'), ('both', 'Both')], max_length=5, null=True)),
                ('antihistamine_120mg', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(0)])),
                ('steroid_tablet', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(0)])),
                ('inhaler', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9), django.core.validators.MinValueValidator(0)])),
                ('nasal_spray_used', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medication.NasalSpray')),
                ('ointment_used', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medication.Ointment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
