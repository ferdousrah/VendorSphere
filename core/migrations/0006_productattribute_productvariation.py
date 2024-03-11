# Generated by Django 4.1.2 on 2024-03-07 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_productimages_product"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "verbose_name_plural": "Product Attributes",
            },
        ),
        migrations.CreateModel(
            name="ProductVariation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=100)),
                (
                    "additional_price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.productattribute",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variations",
                        to="core.product",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Product Variations",
            },
        ),
    ]
