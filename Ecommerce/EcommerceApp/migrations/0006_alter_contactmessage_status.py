# Generated by Django 3.2.3 on 2021-10-14 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcommerceApp', '0005_alter_contactmessage_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='status',
            field=models.CharField(choices=[('Closed', 'Closed'), ('New', 'New'), ('Read', 'Read')], default='New', max_length=40),
        ),
    ]
