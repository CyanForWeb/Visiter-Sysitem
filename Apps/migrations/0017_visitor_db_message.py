# Generated by Django 3.2.20 on 2023-09-04 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps', '0016_remove_other_db_form2_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor_db',
            name='message',
            field=models.TextField(max_length=20, null=True),
        ),
    ]
