# Generated by Django 4.2.6 on 2023-11-28 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_ordereditems_coupon_applied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditems',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]