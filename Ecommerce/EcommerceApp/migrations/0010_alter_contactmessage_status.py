# Generated by Django 3.2.3 on 2021-10-17 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcommerceApp', '0009_auto_20211016_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='status',
            field=models.CharField(choices=[('Read', 'Read'), ('Closed', 'Closed'), ('New', 'New')], default='New', max_length=40),
        ),
    ]
