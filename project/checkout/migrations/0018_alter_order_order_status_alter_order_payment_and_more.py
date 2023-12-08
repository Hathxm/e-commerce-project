# Generated by Django 4.2.6 on 2023-12-07 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0017_alter_usercoupon_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='order_status',
        ),
        migrations.DeleteModel(
            name='payment_method',
        ),
    ]