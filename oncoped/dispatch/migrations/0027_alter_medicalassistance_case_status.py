# Generated by Django 3.2.12 on 2022-03-10 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0026_alter_medicalassistance_case_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalassistance',
            name='case_status',
            field=models.CharField(choices=[('Case Pending', 'Case Pending'), ('Clinic is Ready for takeover', 'Clinic is Ready for takeover'), ('Taken over by Clinic', 'Taken over by Clinic'), ('Taken over previously, in person', 'Taken over previously, in person')], default='Case Pending', max_length=100, verbose_name='Case Status'),
        ),
    ]
