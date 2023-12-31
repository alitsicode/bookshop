# Generated by Django 4.2.3 on 2023-07-05 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('image', models.ImageField(upload_to='product/', verbose_name='image')),
                ('price', models.BigIntegerField(verbose_name='price')),
                ('is_discount', models.BooleanField(default=False, verbose_name='is_discount')),
                ('price_with_discount', models.BigIntegerField(verbose_name='price_with_discount')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('category', models.ManyToManyField(related_name='product', to='pages.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
