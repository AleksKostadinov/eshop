# Generated by Django 4.2.3 on 2023-08-11 13:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0005_productgallery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productgallery',
            options={'verbose_name': 'Product Gallery', 'verbose_name_plural': 'Product Galleries'},
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shop_app.product'),
        ),
    ]
