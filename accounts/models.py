from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html



class Customeuser(AbstractUser):
    email=models.EmailField(_('email'),max_length=254)
    phone=models.CharField(_('phone'),max_length=11,default='09122222222')

    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name=_('CustomeUser') 
        verbose_name_plural=_('CustomeUsers')