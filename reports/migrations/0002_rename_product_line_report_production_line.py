# Generated by Django 4.2.3 on 2023-07-17 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='product_line',
            new_name='production_line',
        ),
    ]
