# Generated by Django 2.0.3 on 2018-05-04 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180504_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='reg_no',
            field=models.CharField(default='', max_length=13, null=True, verbose_name='Organisationsnummer'),
        ),
    ]
