# Generated by Django 4.2.6 on 2023-11-28 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_product_image_cropping'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='discount_percentage',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
    ]