# Generated by Django 4.2.3 on 2024-06-28 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_childcategory_product_child_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='child_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childcategory', to='product.childcategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='product.subcategory'),
        ),
    ]
