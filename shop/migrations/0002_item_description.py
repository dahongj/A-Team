# Generated by Django 4.2.9 on 2024-04-15 10:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="description",
            field=models.CharField(default="an item", max_length=200),
        ),
    ]
