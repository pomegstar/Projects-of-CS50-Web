# Generated by Django 5.0.7 on 2024-08-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0003_appointment_is_complete_appointment_problem"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="age",
            field=models.PositiveIntegerField(null=True),
        ),
    ]
