# Generated by Django 4.2.3 on 2023-08-07 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_shipping_cost_percent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_cost_percent',
        ),
    ]