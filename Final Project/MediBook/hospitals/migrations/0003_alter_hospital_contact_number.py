# Generated by Django 5.0.7 on 2024-08-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospitals", "0002_doctor_fro_doctor_to_doctor_weeks"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hospital",
            name="contact_number",
            field=models.PositiveIntegerField(max_length=15),
        ),
    ]
