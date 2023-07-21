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

class Colors(models.Model):
    color=models.CharField(_("رنگ"), max_length=70)
    

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

    def __str__(self):
        return self.color

class Size(models.Model):
    size=models.CharField(_("سایز"), max_length=70)
    

    class Meta:
        verbose_name = _("سایز")
        verbose_name_plural = _("سایز ها")

    def __str__(self):
        return self.size





class Product(models.Model):
    title=models.CharField(_("title"), max_length=100)
    description=models.TextField(_("description"))
    category=models.ManyToManyField(Category, verbose_name=_("category"),related_name='product')
    color=models.ManyToManyField(Colors, verbose_name=_("رنگ"),blank=True,null=True)
    size=models.ForeignKey(Size, verbose_name=_("سایز"), on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField(_("image"), upload_to='product/')
    price=models.BigIntegerField(_("price (rial)"))
    is_discount=models.BooleanField(_("is_discount"),default=False,null=True,blank=True)
    price_with_discount=models.BigIntegerField(_("price_with_discount (rial)"),null=True,blank=True)
    created=models.DateTimeField(_("created"), auto_now_add=True)
    updated=models.DateTimeField(_("updated"), auto_now=True)
    

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def image_tag(self):
        return format_html('<img width=100px height=100px src="{}" />'. format(self.image.url))

    def __str__(self):
        return self.title


class AboutUs(models.Model):
    site_name=models.CharField(_("site_name"), max_length=100)
    logo=models.ImageField(_("logo"), upload_to='site_logo/')
    site_description=models.TextField(_("site_description"))
    whatsapp_number=models.CharField(_("whatsapp_number(no 0)"), max_length=10,null=True,blank=True)
    telegram_id=models.CharField(_("telegram_id"), max_length=50,null=True,blank=True)
    instagram_id=models.CharField(_("instagram_id"), max_length=50)
    phone_number=models.CharField(_("phone_number"), max_length=11,null=True,blank=True)
    created=models.DateTimeField(_("created"), auto_now_add=True)
    updated=models.DateTimeField(_("updated"), auto_now=True)

    class Meta:
        verbose_name = _("AboutUs")
        verbose_name_plural = _("AboutUs")

    def __str__(self):
        return self.site_name
