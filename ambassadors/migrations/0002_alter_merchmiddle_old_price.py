# Generated by Django 4.2.10 on 2024-02-26 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ambassadors", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="merchmiddle",
            name="old_price",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Архивная цена"
            ),
        ),
    ]
