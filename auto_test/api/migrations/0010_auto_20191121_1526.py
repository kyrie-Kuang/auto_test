# Generated by Django 2.1.3 on 2019-11-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20191121_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apis',
            name='api_method',
            field=models.CharField(choices=[('0', 'get'), ('1', 'post')], default='0', max_length=200),
        ),
    ]
