# Generated by Django 3.2.20 on 2023-08-04 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apps', '0010_auto_20230804_1940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='other_db',
            old_name='fomr2_address',
            new_name='form2_address',
        ),
        migrations.RenameField(
            model_name='other_db',
            old_name='fomr2_contact',
            new_name='form2_contact',
        ),
        migrations.RenameField(
            model_name='other_db',
            old_name='fomr2_name',
            new_name='form2_name',
        ),
    ]
