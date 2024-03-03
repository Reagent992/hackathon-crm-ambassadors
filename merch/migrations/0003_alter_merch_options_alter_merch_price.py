# Generated by Django 4.2.10 on 2024-02-26 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "merch",
            "0002_merch_created_merch_updated_alter_merch_article_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="merch",
            options={
                "ordering": ("title",),
                "verbose_name": "Мерч",
                "verbose_name_plural": "Мерч",
            },
        ),
        migrations.AlterField(
            model_name="merch",
            name="price",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Цена"
            ),
        ),
    ]