# Generated by Django 4.2.6 on 2023-10-25 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_remove_order_items_remove_order_user_delete_payment_and_more'),
        ('checkout', '0018_alter_order_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='user.cartitem'),
        ),
    ]
