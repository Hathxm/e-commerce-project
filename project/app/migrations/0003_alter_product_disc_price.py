# Generated by Django 4.2.5 on 2023-10-14 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_brand_category_gender_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='disc_price',
            field=models.IntegerField(null=True, verbose_name='discount price'),
        ),
    ]
