# Generated by Django 4.2 on 2023-04-22 20:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_order_executor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passportinfo',
            name='passport_series',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(1000)], verbose_name='passport series'),
        ),
    ]