# Generated by Django 2.1.3 on 2019-11-18 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20191115_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='p_create_time',
            new_name='create_time',
        ),
    ]
