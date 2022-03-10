# Generated by Django 3.2.12 on 2022-03-10 21:07

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0032_auto_20220310_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientrequest',
            name='therapy_needs',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('CHE', 'Chemotherapy'), ('SUR', 'Surgical'), ('PAL', 'Palliative'), ('MON', 'Monitoring'), ('INV', 'Diagnostic Investigation'), ('SUT', 'Supportive Treatment'), ('RAD', 'Radiotherapy'), ('TRA', 'Transplant'), ('OTH', 'Other')], max_length=35, verbose_name='Therapy Needs'),
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='tumor_type',
            field=models.CharField(blank=True, choices=[('S', 'Solid'), ('H', 'Hematologic')], max_length=2, verbose_name='Tumor Type'),
        ),
    ]
