# Generated by Django 5.0.7 on 2024-08-08 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_patient_contact_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="contact_number",
            field=models.PositiveIntegerField(null=True),
        ),
    ]
