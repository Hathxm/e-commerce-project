# Generated by Django 4.2.6 on 2023-11-05 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_product_in_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('total_sales', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('quantity_sold', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
