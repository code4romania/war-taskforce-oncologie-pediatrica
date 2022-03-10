# Generated by Django 3.2.12 on 2022-03-10 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0031_auto_20220310_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientrequest',
            name='child_current_address',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Child Current Address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='child_current_city',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Child Current City'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='child_current_country',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Child Current Country'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='child_current_county',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Child Current County'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='complete_diagnostic',
            field=models.TextField(blank=True, default='', verbose_name='Complete Diagnostic'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='current_clinical_status',
            field=models.TextField(blank=True, default='', verbose_name='Current Clinical Status'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='diagnosing_institution_name',
            field=models.CharField(blank=True, default='', max_length=150, verbose_name='Diagnosing Institution Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='estimated_arrival_dt',
            field=models.DateTimeField(null=True, verbose_name='Estimated Arrival'),
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='general_problem_description',
            field=models.TextField(blank=True, default='', help_text="Describe the Child's medical issue", verbose_name='General Problem Description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='institution_name',
            field=models.CharField(blank=True, default='', help_text='Fill in only if requester is not a Person', max_length=250, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='origin_medical_institution_contact_person',
            field=models.CharField(blank=True, default='', help_text='Full Name of the contact person', max_length=150, verbose_name='Contact Person'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='origin_medical_institution_email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='Email'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='origin_medical_institution_name',
            field=models.CharField(blank=True, default='', max_length=150, verbose_name='Institution Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='origin_medical_institution_phone_number',
            field=models.CharField(blank=True, default='', help_text="Contact Person's phone number. Please include country prefix e.g. +40723000123", max_length=30, verbose_name='Phone Number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientrequest',
            name='other_therapy_needs',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='Other Therapy Needs'),
            preserve_default=False,
        ),
    ]
