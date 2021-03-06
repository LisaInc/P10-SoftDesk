# Generated by Django 4.0.2 on 2022-03-04 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("back", "back-end"),
                            ("front", "front-end"),
                            ("ios", "iOS"),
                            ("android", "Android"),
                        ],
                        max_length=255,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Contributor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "permission",
                    models.CharField(
                        choices=[("author", "author"), ("contributor", "Contributor")],
                        max_length=255,
                    ),
                ),
                ("role", models.CharField(max_length=255)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.project"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
