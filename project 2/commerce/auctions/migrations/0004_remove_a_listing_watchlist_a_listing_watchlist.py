# Generated by Django 5.0.6 on 2024-06-13 00:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_a_listing_watchlist"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="a_listing",
            name="watchlist",
        ),
        migrations.AddField(
            model_name="a_listing",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="watch", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
