# Generated by Django 4.2.4 on 2024-01-19 17:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0009_customer_otp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="Address_type",
            field=models.CharField(max_length=6),
        ),
    ]
