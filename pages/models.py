from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
# Create your models here.

class Category(models.Model):
    title=models.CharField(_("title"), max_length=100)
    cover=models.ImageField(_("cover"), upload_to='category/')
    created=models.DateTimeField(_("created"), auto_now_add=True)
    updated=models.DateTimeField(_("updated"), auto_now=True)
    

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def cover_tag(self):
        return format_html('<img width=100px height=100px src="{}" />'. format(self.cover.url))
    def __str__(self):
        return self.title



class Product(models.Model):
    title=models.CharField(_("title"), max_length=100)
    description=models.TextField(_("description"))
    category=models.ManyToManyField(Category, verbose_name=_("category"),related_name='product')
    image=models.ImageField(_("image"), upload_to='product/')
    price=models.BigIntegerField(_("price"))
    is_discount=models.BooleanField(_("is_discount"),default=False,null=True,blank=True)
    price_with_discount=models.BigIntegerField(_("price_with_discount"),null=True,blank=True)
    created=models.DateTimeField(_("created"), auto_now_add=True)
    updated=models.DateTimeField(_("updated"), auto_now=True)
    

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def image_tag(self):
        return format_html('<img width=100px height=100px src="{}" />'. format(self.image.url))

    def __str__(self):
        return self.title



