# Generated by Django 4.2.6 on 2023-10-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_customuser_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
