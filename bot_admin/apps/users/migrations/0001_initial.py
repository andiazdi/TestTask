# Generated by Django 5.2.1 on 2025-05-27 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TelegramUser",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("telegram_id", models.BigIntegerField(unique=True)),
                ("username", models.CharField(blank=True, max_length=255)),
                ("first_name", models.CharField(blank=True, max_length=255)),
                ("last_name", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "db_table": "users",
            },
        ),
    ]
