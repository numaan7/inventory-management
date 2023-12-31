# Generated by Django 4.2.2 on 2023-08-06 14:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_invoice_invoice_pdf_alter_invoice_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 19, 54, 1, 364517)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 19, 54, 1, 359429)),
        ),
        migrations.AlterField(
            model_name='invoice_item',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 19, 54, 1, 357461)),
        ),
        migrations.AlterField(
            model_name='ledger',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 19, 54, 1, 366481)),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 19, 54, 1, 354823)),
        ),
    ]
