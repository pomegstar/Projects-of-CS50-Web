# Generated by Django 5.0.6 on 2024-07-01 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_posts"),
    ]

    operations = [
        migrations.AlterField(
            model_name="posts",
            name="Like",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="posts",
            name="post",
            field=models.TextField(blank=True),
        ),
    ]
