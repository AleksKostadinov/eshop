# Generated by Django 4.2.3 on 2023-08-15 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0010_remove_product_additional_discount_percentage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='additional_discount_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
