# Generated by Django 4.2.3 on 2023-07-10 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_orderitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_total_price',
            field=models.IntegerField(default=0, verbose_name='total_price'),
        ),
    ]
