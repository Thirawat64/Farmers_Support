# Generated by Django 5.0.6 on 2024-05-30 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_alter_sell_buy_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="sell_buy",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]