# Generated by Django 4.2.3 on 2023-07-17 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_alter_discountcode_user_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tracking_code',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='کد رهگیری پست'),
        ),
    ]
