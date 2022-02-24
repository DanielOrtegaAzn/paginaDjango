from ctypes import sizeof
from django import forms
from nucleo.models import Employee

class employeeForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields=['dni','name','surname','address','biography']
        widgets={
            "dni":forms.TextInput(attrs={"class":"form-control"}),
            "name":forms.TextInput(attrs={"name":"nombre", "class":"form-control"}),
            "surname":forms.TextInput(attrs={"class":"form-control"}),
            "address":forms.TextInput(attrs={"class":"form-control"}),
            "biography":forms.Textarea(attrs={"class":"form-control",'rows':5,'columns':10})
        }