# Generated by Django 4.2.3 on 2023-07-20 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_remove_discountcode_discount_percent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcode',
            name='discount_price1',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name=' خرید 500.000 تومان و بیشتر (تخفیف را به ریال وارد کنید)'),
        ),
        migrations.AlterField(
            model_name='discountcode',
            name='discount_price2',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name=' خرید 1.000.000 تومان و بیشتر (تخفیف را به ریال وارد کنید)'),
        ),
        migrations.AlterField(
            model_name='discountcode',
            name='discount_price3',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name=' خرید 2.000.000 تومان و بیشتر (تخفیف را به ریال وارد کنید)'),
        ),
    ]
