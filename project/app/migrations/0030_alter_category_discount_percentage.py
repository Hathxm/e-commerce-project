# Generated by Django 4.2.6 on 2023-12-04 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_alter_category_valid_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='discount_percentage',
            field=models.FloatField(default=0),
        ),
    ]