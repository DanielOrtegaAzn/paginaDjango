from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from registration.forms import clientForm, userForm
    
'''class SignupView(CreateView):
    form_class=UserCreationForm
    template_name='registration/registro.html'
    
    def get_success_url(self):
        return reverse_lazy('login')+'?register'
    
    def get_form(self,form_class=None):
        form=super(SignupView,self).get_form()
        form.fields['username'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                       'placeholder':'Usuario'})
        form.fields['password1'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
                                                                   'placeholder':'Contraseña'})
        form.fields['password2'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
                                                                   'placeholder':'Repite la contraseña'})
        return form'''

def client(request):
    if request.method =="POST":
        user_form=userForm(data=request.POST)
        client_form=clientForm(data=request.POST)
        if client_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            password=user_form.cleaned_data['password']
            user.set_password(password)
            user.is_client = True
            user.save()
            client = client_form.save(commit=False)
            client.userId=user
            client.save()
            return redirect("/accounts/login/")
    else:
        user_form=userForm()
        client_form=clientForm()
        
    return render(request,"registration/registro.html",{"user_form":user_form,"client_form":client_form})