# Generated by Django 5.0.6 on 2024-06-13 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_bids_bid_bids_bidder_alter_a_listing_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bids",
            name="bid",
            field=models.IntegerField(default=0),
        ),
    ]
