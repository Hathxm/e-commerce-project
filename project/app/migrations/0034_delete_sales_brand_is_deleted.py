# Generated by Django 4.2.6 on 2023-12-06 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_alter_product_frontimg_alter_product_img_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sales',
        ),
        migrations.AddField(
            model_name='brand',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
