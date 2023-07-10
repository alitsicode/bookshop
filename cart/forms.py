from django import forms
    
class add_to_cart_form(forms.Form):
    quantity_choice=[
        (i,str(i)) for i in range(1,31)
    ]
    quantity=forms.TypedChoiceField(choices=quantity_choice,coerce=int)
    # make diffrent add or inplace quantity of product in add to cart/detail template
    inplace=forms.BooleanField(required=False,widget=forms.HiddenInput)