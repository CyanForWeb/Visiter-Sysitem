# Generated by Django 3.2.20 on 2023-10-06 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps', '0023_auto_20231005_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner_db',
            name='update_url_text',
            field=models.TextField(max_length=8, null=True),
        ),
    ]