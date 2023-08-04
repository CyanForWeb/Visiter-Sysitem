# Generated by Django 3.2.20 on 2023-08-04 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps', '0003_auto_20230804_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery_DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor', models.TextField(default='Delivery')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='delivery_image')),
            ],
        ),
        migrations.AlterField(
            model_name='appt_db',
            name='visitor',
            field=models.TextField(default='Appt'),
        ),
    ]
