from django.contrib import admin
from .models import Customeuser
from accounts.forms import customuserchangeform,customusercreationform
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class customuseradmin(UserAdmin):
    add_form=customusercreationform
    form=customuserchangeform
    model=Customeuser
    fieldsets=UserAdmin.fieldsets+(
        (None,{'fields':('phone',)},),
    )
    add_fieldsets=UserAdmin.add_fieldsets+(
        (None,{'fields':('email','phone')},),
    )
    
admin.site.register(Customeuser,customuseradmin)