# Generated by Django 3.2.20 on 2023-11-01 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apps', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='other_db',
            old_name='form2_address',
            new_name='form2_contact',
        ),
    ]