# Generated by Django 5.0.6 on 2024-06-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_sell_buy_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="sell_buy",
            name="sell_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
