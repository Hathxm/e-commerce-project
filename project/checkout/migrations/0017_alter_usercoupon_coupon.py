# Generated by Django 4.2.6 on 2023-12-07 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0016_alter_usercoupon_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercoupon',
            name='coupon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.coupon'),
        ),
    ]
