from django.contrib import admin
from django import forms
from registration.models import Usuario
from nucleo.admin import EmployeeInLine,ClientInLine

class UsuarioAdminForm(forms.ModelForm):
    pass

class UsuarioInLine(admin.StackedInline):
    model=Usuario
    
class UsuarioAdmin(admin.ModelAdmin):
    form=UsuarioAdminForm
    list_per_page=8
    ordering=["pk"]
    list_display=["username"]
    inlines=[EmployeeInLine,ClientInLine,]

admin.site.register(Usuario,UsuarioAdmin)