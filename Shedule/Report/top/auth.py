from django import forms
 
class AuthForm(forms.Form):
    login = forms.CharField(required=True)
    password = forms.CharField(required=True)