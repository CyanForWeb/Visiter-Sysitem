# Generated by Django 3.2.20 on 2023-08-04 10:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Apps', '0005_alter_delivery_db_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery_db',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]