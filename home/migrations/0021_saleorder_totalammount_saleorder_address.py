# Generated by Django 4.2.4 on 2024-03-04 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0020_alter_address_landmark"),
    ]

    operations = [
        migrations.AddField(
            model_name="saleorder",
            name="Totalammount",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="saleorder",
            name="address",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="home.address",
            ),
        ),
    ]
