# Generated by Django 4.2.6 on 2023-11-28 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_remove_coupon_user_usercoupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='checkout.order_status'),
        ),
    ]
