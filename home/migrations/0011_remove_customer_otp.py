# Generated by Django 4.2.4 on 2024-01-19 18:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0010_alter_address_address_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="otp",
        ),
    ]
