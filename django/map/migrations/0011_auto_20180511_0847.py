# Generated by Django 2.0.3 on 2018-05-11 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0010_auto_20180511_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='price_date',
            field=models.CharField(default='', max_length=8, null=True, verbose_name='Försäljningsdatum'),
        ),
    ]
