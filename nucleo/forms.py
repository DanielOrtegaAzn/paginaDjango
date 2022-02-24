from multiprocessing.connection import Client
from django import forms
from registration.forms import DateInput

from nucleo.models import Client, Participate,Proyect
from registration.models import Usuario

class clientForm(forms.ModelForm):
    class Meta:
        model=Client
        fields = ['dni', 'name', 'surname', 'address', 'birthday']
        widgets= {
            "birthday":DateInput(),
        }

class userUpdateForm(forms.ModelForm):
    class Meta:
        model=Usuario
        fields=["password"]
        widgets= {
            "password":forms.PasswordInput(attrs={"class":"form-control",
                    "placeholder":"Escribe aqui la nueva contraseña, en caso de querer cambiarla"})
        }
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(userUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['password'].required = False
    
class clientUpdateForm(forms.ModelForm):
    class Meta:
        model=Client
        fields=['dni','name','surname','address','birthday']
        widgets= {
            "birthday":forms.DateInput(format='%d/%m/%Y',attrs={'placeholder':'dia/mes/año'})
        }

class ProyectForm(forms.ModelForm):
    class Meta:
        model = Proyect
        fields = ['title', 'description', 'level', 'startDate', 'endDate', 'categoryId']
        widgets= {
            "startDate":forms.DateInput(format='%d/%m/%Y',attrs={'placeholder':'dia/mes/año'}),
            "endDate":forms.DateInput(format='%d/%m/%Y',attrs={'placeholder':'dia/mes/año'})
        }
        
class ProyectUpdateForm(forms.ModelForm):
    class Meta:
        model = Proyect
        fields = ['title', 'description', 'level', 'startDate', 'endDate', 'categoryId']
        widgets= {
            "startDate":forms.DateInput(format='%d/%m/%Y',attrs={'placeholder':'dia/mes/año'}),
            "endDate":forms.DateInput(format='%d/%m/%Y',attrs={'placeholder':'dia/mes/año'})
        }
        
class ParticipateRoleForm(forms.ModelForm):
    class Meta:
        model = Participate
        fields = ["role"]

class endProyectForm(forms.ModelForm):
    class Meta:
        model = Proyect
        fields = ['endingReport']
        widgets={
            "endingReport":forms.Textarea(attrs={"class":"form-control",'rows':5,'columns':10})
        }