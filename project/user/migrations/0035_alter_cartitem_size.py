# Generated by Django 4.2.6 on 2023-10-25 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_product_frontimg_product_rearimg'),
        ('user', '0034_cartitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='size',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='app.size'),
        ),
    ]
