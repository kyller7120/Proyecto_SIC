# Generated by Django 4.2.7 on 2023-11-07 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codesoftapp', '0010_utilidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_capital', models.DecimalField(decimal_places=2, max_digits=10)),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codesoftapp.periodo')),
            ],
        ),
    ]
