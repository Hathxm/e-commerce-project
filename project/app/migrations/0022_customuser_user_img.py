# Generated by Django 4.2.6 on 2023-11-12 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_product_disc_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_img',
            field=models.ImageField(null=True, upload_to='user_pics'),
        ),
    ]
