from django.contrib.auth.models import User
from django import forms
from django.forms import widgets
from django.forms.widgets import DateInput, PasswordInput

from nucleo.models import Client
from registration.models import Usuario

class userForm(forms.ModelForm):
    class Meta:
        model=Usuario
        fields=["username","password"]
        widgets= {
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"})
        }

class DateInput(forms.DateInput):
    input_type= 'date'
    
class clientForm(forms.ModelForm):
    class Meta:
        model=Client
        fields=['dni','name','surname','address','birthday']
        widgets= {
            "birthday":DateInput(),
        }