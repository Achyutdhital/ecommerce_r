# Generated by Django 4.2.3 on 2024-06-30 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dateofbirth',
            field=models.DateField(blank=True, null=True),
        ),
    ]