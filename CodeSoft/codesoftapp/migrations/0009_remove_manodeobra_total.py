# Generated by Django 4.2.6 on 2023-10-25 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codesoftapp', '0008_manodeobra_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manodeobra',
            name='total',
        ),
    ]
