# Generated by Django 3.2.12 on 2022-03-11 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0006_auto_20220311_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalassistance',
            name='location',
            field=models.TextField(blank=True, help_text='Location: City, Country', max_length=250, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='known_complete_diagnostic',
            field=models.CharField(default=0, max_length=2, verbose_name='Complete Diagnostic Known'),
        ),
    ]
