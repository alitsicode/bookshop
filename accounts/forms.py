from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from . models import Customeuser
from django import forms

class customusercreationform(UserCreationForm):
    class Meta:
        model=Customeuser
        fields=UserCreationForm.Meta.fields + ('phone',)

class customuserchangeform(UserChangeForm):
    class Meta:
        model=Customeuser
        fields=UserChangeForm.Meta.fields
