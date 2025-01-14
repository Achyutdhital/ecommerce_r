# Generated by Django 4.2.3 on 2024-07-08 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('Qatar', 'Qatar'), ('Oman', 'Oman'), ('Dubai', 'Dubai')], max_length=20)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('streetnumber', models.CharField(max_length=200)),
                ('warehousename', models.CharField(max_length=300)),
                ('contact', models.CharField(max_length=20)),
            ],
        ),
    ]
