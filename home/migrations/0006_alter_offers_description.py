# Generated by Django 4.2.4 on 2024-01-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0005_restaurant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offers",
            name="Description",
            field=models.TextField(unique=True),
        ),
    ]
