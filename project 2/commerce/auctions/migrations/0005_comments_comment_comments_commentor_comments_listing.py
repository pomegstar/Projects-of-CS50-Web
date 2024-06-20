# Generated by Django 5.0.6 on 2024-06-13 05:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_remove_a_listing_watchlist_a_listing_watchlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="comments",
            name="comment",
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="comments",
            name="commentor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commentor",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comments",
            name="listing",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="listing",
                to="auctions.a_listing",
            ),
        ),
    ]
