# Generated by Django 2.1.7 on 2019-04-21 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybank', '0002_auto_20190420_1632'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['t_dttm']},
        ),
    ]
