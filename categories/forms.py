from distutils.command.upload import upload
from django import forms
from django.db import models
from nucleo.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=["name","photo"]
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
        }