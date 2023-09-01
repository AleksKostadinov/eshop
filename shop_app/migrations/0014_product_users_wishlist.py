# Generated by Django 4.2.3 on 2023-08-31 20:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop_app", "0013_cover"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="users_wishlist",
            field=models.ManyToManyField(
                blank=True,
                related_name="add_remove_wishlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]