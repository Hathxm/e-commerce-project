# Generated by Django 4.2.6 on 2023-11-28 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_ordereditems_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditems',
            name='total',
            field=models.BigIntegerField(),
        ),
    ]