# Generated by Django 4.1.5 on 2023-07-31 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_cost_percent',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
