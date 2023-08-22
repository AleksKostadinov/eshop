# Generated by Django 4.2.3 on 2023-08-21 08:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribedUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
            ],
        ),
    ]