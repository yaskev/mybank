# Generated by Django 2.1.7 on 2019-04-16 20:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mybank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionhistory',
            name='transaction_dttm',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 16, 20, 40, 2, 581295, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='join_dt',
            field=models.DateField(default=datetime.datetime(2019, 4, 16, 20, 40, 2, 579988, tzinfo=utc)),
        ),
    ]
