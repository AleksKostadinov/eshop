# Generated by Django 4.1.5 on 2023-07-31 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_shipping_cost_percent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_cost_percent', models.FloatField()),
            ],
        ),
    ]