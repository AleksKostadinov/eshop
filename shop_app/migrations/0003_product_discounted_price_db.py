# Generated by Django 4.2.3 on 2023-08-09 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0002_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discounted_price_db',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]