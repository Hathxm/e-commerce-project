# Generated by Django 4.2.6 on 2023-10-23 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_img_product_img1_product_img2_product_img3'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discription',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
