# Generated by Django 4.2.3 on 2024-07-01 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_remove_childcategory_category_subcategory_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannar',
            name='title',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
