# Generated by Django 5.0.6 on 2024-07-06 09:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0006_remove_user_follower_remove_user_following_follow"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="posts",
            name="like",
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "liked_post",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="liked",
                        to="network.posts",
                    ),
                ),
                (
                    "liker",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="liker",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
