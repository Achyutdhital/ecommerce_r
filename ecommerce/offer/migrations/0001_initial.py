# Generated by Django 4.2.3 on 2024-07-09 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0015_merge_20240707_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupontitle', models.CharField(max_length=150, verbose_name='Coupon Title')),
                ('coupon_code', models.CharField(max_length=50, verbose_name='Coupon Code')),
                ('discount_on', models.CharField(choices=[('all_product', 'All Product'), ('category', 'Category'), ('sub_category', 'Sub Category'), ('product', 'Product')], max_length=50, verbose_name='Discount On')),
                ('discount', models.FloatField(verbose_name='Discount')),
                ('coupon_type', models.CharField(choices=[('percentage', 'Percentage'), ('fixed_amount', 'Fixed Amount')], max_length=50, verbose_name='Coupon Type')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('expired_date', models.DateField(verbose_name='Expired Date')),
                ('coupon_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=50, verbose_name='Coupon Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_category', to='product.category')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_item', to='product.product')),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_sub_category', to='product.subcategory')),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
            },
        ),
    ]