# Generated by Django 4.2.4 on 2024-01-30 15:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0014_customer_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customer",
            old_name="Image",
            new_name="cus_Image",
        ),
    ]
