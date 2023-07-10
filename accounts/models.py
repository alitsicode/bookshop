from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html



class Customeuser(AbstractUser):
    email=models.EmailField(_('email'),max_length=254,unique=True)
    phone=models.CharField(_('phone'),max_length=11,null=True,blank=True)

    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name=_('CustomeUser') 
        verbose_name_plural=_('CustomeUsers')