from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from . models import Customeuser
from django import forms
from allauth.account.forms import SignupForm

class customusercreationform(UserCreationForm):
    class Meta:
        model=Customeuser
        fields=UserCreationForm.Meta.fields + ('phone',)

class customuserchangeform(UserChangeForm):
    class Meta:
        model=Customeuser
        fields=UserChangeForm.Meta.fields

class MyCustomSignupForm(SignupForm):
    phone = forms.CharField(max_length=11)
    email = forms.EmailField(required=True)
    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.
        user.phone = self.cleaned_data['phone']
        user.email = self.cleaned_data['email']
        user.save()
        # You must return the original result.
        return user