# Generated by Django 4.2.3 on 2023-07-09 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_discountcode_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcode',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
    ]
