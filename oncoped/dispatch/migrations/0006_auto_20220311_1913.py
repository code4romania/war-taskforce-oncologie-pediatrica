# Generated by Django 3.2.12 on 2022-03-11 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0005_auto_20220311_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalassistance',
            name='country',
        ),
        migrations.RemoveField(
            model_name='medicalassistance',
            name='town',
        ),
        migrations.AddField(
            model_name='medicalassistance',
            name='location',
            field=models.TextField(blank=True, max_length=250, verbose_name='Location'),
        ),
    ]
