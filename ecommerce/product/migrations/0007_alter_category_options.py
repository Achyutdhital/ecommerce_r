# Generated by Django 4.2.3 on 2024-06-25 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_rename_price_stock_addprice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-ordering', '-id']},
        ),
    ]
