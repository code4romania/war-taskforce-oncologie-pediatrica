# Generated by Django 3.2.12 on 2022-03-11 09:34

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.CharField(choices=[('patient_request', 'Patient request form email')], max_length=254, unique=True, verbose_name='Template')),
                ('text_content', models.TextField(verbose_name='Text content')),
                ('html_content', ckeditor.fields.RichTextField(blank=True, verbose_name='HTML content')),
            ],
            options={
                'verbose_name': 'Email template',
                'verbose_name_plural': 'Email templates',
            },
        ),
    ]
