# Generated by Django 4.2.6 on 2023-12-03 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_ordereditems_total'),
        ('checkout', '0010_alter_order_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user.ordereditems'),
            preserve_default=False,
        ),
    ]
