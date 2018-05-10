# Generated by Django 2.0.3 on 2018-05-10 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0013_auto_20180509_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='block',
            field=models.CharField(default='', max_length=4, verbose_name='Block'),
        ),
        migrations.AddField(
            model_name='property',
            name='district',
            field=models.CharField(default='', max_length=40, verbose_name='Trakt'),
        ),
        migrations.AddField(
            model_name='property',
            name='sign',
            field=models.CharField(default='', max_length=1, null=True, verbose_name='Tecken'),
        ),
        migrations.AddField(
            model_name='property',
            name='unity',
            field=models.CharField(default='', max_length=4, verbose_name='Enhet'),
        ),
    ]
