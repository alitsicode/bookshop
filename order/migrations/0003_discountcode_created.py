# Generated by Django 4.2.3 on 2023-07-09 19:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_discountcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountcode',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
    ]