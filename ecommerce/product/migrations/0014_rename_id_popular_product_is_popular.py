# Generated by Django 4.2.3 on 2024-07-04 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_product_id_popular_product_is_featured'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='id_popular',
            new_name='is_popular',
        ),
    ]
