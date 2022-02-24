from asyncio.windows_events import NULL
from django.contrib import admin
from django import forms
from nucleo.models import Category, Client, Employee, Participate, Proyect

#Participate
class ParticipateAdminForm(forms.ModelForm):
    def clean_clientId(self):
        if (self.cleaned_data['clientId'] == NULL):
            raise forms.ValidationError('El id del cliente no puede ser nulo')
        else:
            return self.cleaned_data['clientId']
        
    def clean_proyectId(self):
        if (self.cleaned_data['proyectId'] == NULL):
            raise forms.ValidationError('El id del proyecto no puede ser nulo')
        else:
            return self.cleaned_data['proyectId']
    
    def clean_role(self):
        if (len(self.cleaned_data['role'])>100):
            raise forms.ValidationError('El rol no puede tener mas de 100 caracteres')
        else:
            return self.cleaned_data['role']

class ParticipateAdmin(admin.ModelAdmin):
    form=ParticipateAdminForm
    list_per_page=10
    ordering=["inscriptionDate"]
    list_filter=["inscriptionDate","proyectId","clientId","role"]
    list_display=["clientId","proyectId","role","inscriptionDate"]

class ParticipateInLine(admin.StackedInline):
    model=Participate
    
#Proyect
class ProyectAdminForm(forms.ModelForm):
    def clean_name(self):
        if (len(self.cleaned_data['title'])<2):
            raise forms.ValidationError('El titulo debe tener mas de un caracter')
        else:
            return self.cleaned_data['titulo']
        
    def clean_description(self):
        if (len(self.cleaned_data['description'])>255):
            raise forms.ValidationError('La descripcion no puede tener mas de 255 caracteres')
        else:
            return self.cleaned_data['description']

class ProyectInLine(admin.StackedInline):
    model=Proyect

class ProyectAdmin(admin.ModelAdmin):
    form=ProyectAdminForm
    list_per_page=10
    ordering=["startDate"]
    list_filter=["level","startDate","endDate","employeeId","categoryId"]
    list_display=["id","title","level","startDate","endDate"]
    inlines=[ParticipateInLine,]
    
#Employee
class EmployeeAdminForm(forms.ModelForm):
    def clean_dni(self):
        if (len(self.cleaned_data['dni'])>9):
            raise forms.ValidationError('El dni no puede tener mas de 9 caracteres')
        else:
            return self.cleaned_data['dni']
    def clean_name(self):
        if(len(self.cleaned_data['name'])>40):
            raise forms.ValidationError('El nombre no puede tener mas de 40 caracteres')
        else:
            return self.cleaned_data['name']
    def clean_surname(self):
        if(len(self.cleaned_data['surname'])>60):
            raise forms.ValidationError('El apellido no puede tener mas de 60 caracteres')
        else:
            return self.cleaned_data['surname']
    def clean_address(self):
        if(len(self.cleaned_data['address'])>150):
            raise forms.ValidationError('La direccion no puede tener mas de 150 caracteres')
        else:
            return self.cleaned_data['address']
    def clean_biography(self):
        if(len(self.cleaned_data['biography'])>60):
            raise forms.ValidationError('La biografia no puede tener mas de 255 caracteres')
        else:
            return self.cleaned_data['biography']
    def clean_userId(self):
        if(self.cleaned_data['userId']==NULL):
            raise forms.ValidationError('El id de usuario no puede ser nulo')
        else:
            return self.cleaned_data['userId']

class EmployeeInLine(admin.StackedInline):
    model=Employee

class EmployeeAdmin(admin.ModelAdmin):
    form=EmployeeAdminForm
    list_per_page=8
    list_display=["dni","userId"]
    inlines=[ProyectInLine,]
    
#Client
class ClientAdminForm(forms.ModelForm):
    def clean_dni(self):
        if (len(self.cleaned_data['dni'])>9):
            raise forms.ValidationError('El dni no puede tener mas de 9 caracteres')
        else:
            return self.cleaned_data['dni']
    def clean_name(self):
        if(len(self.cleaned_data['name'])>40):
            raise forms.ValidationError('El nombre no puede tener mas de 40 caracteres')
        else:
            return self.cleaned_data['name']
    def clean_surname(self):
        if(len(self.cleaned_data['surname'])>60):
            raise forms.ValidationError('El apellido no puede tener mas de 60 caracteres')
        else:
            return self.cleaned_data['surname']
    def clean_address(self):
        if(len(self.cleaned_data['address'])>150):
            raise forms.ValidationError('La direccion no puede tener mas de 150 caracteres')
        else:
            return self.cleaned_data['address']
    def clean_userId(self):
        if(self.cleaned_data['userId']==NULL):
            raise forms.ValidationError('El id de usuario no puede ser nulo')
        else:
            return self.cleaned_data['userId']

class ClientInLine(admin.StackedInline):
    model=Client

class ClientAdmin(admin.ModelAdmin):
    form=ClientAdminForm
    list_per_page=8
    ordering=["fechaAlta"]
    list_filter=["birthday","fechaAlta"]
    list_display=["dni","userId","fechaAlta"]
    inlines=[ParticipateInLine,]

#Category
class CategoryAdminForm(forms.ModelForm):
    def clean_name(self):
        if (len(self.cleaned_data['name'])>150):
            raise forms.ValidationError('El no puede tener mas de 150 caracteres')
        else:
            return self.cleaned_data['name']

class CategoryInLine(admin.StackedInline):
    model=Category

class CategoryAdmin(admin.ModelAdmin):
    form=CategoryAdminForm
    list_per_page=10
    ordering=["name"]
    list_display=["name","photo"]
    inlines=[ProyectInLine,]

# Register your models here.
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(Proyect,ProyectAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Participate,ParticipateAdmin)
