# Generated by Django 4.2.4 on 2024-01-30 15:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0013_remove_customer_address_landmark_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="Image",
            field=models.ImageField(null=True, upload_to="photos"),
        ),
    ]
