from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect,render
from adminApp.decorators import admin_required
from adminApp.forms import employeeForm
from nucleo.forms import userUpdateForm
from nucleo.models import Employee
from registration.forms import userForm
from registration.models import Usuario
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

@method_decorator([login_required,admin_required], name="dispatch")
class EmployeeListView(ListView):
    model=Employee
    fields=["dni","name","address","biography"]

@login_required
@admin_required
def employee(request):
    if request.method =="POST":
        user_form=userForm(data=request.POST)
        employee_form=employeeForm(data=request.POST)
        if employee_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            password=user_form.cleaned_data['password']
            user.set_password(password)
            user.is_employee = True
            user.save()
            employee = employee_form.save(commit=False)
            employee.userId=user
            employee.save()
            messages.success(request,"El empleado se ha creado con exito")
            return redirect("/adminViews/listEmployee")
    else:
        user_form=userForm()
        employee_form=employeeForm()
        
    return render(request,"adminApp/employee_form.html",{"user_form":user_form,"employee_form":employee_form})

@login_required
@admin_required
def updateEmployee(request,pk):
    employee=Employee.objects.get(pk=pk)
    user=get_object_or_404(Usuario,username=getattr(employee, 'userId'))
    oldPassword=user.password
    
    if request.method =="POST":
        user_form=userUpdateForm(data=request.POST,instance=user)
        employee_form=employeeForm(data=request.POST,instance=employee)
        if employee_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            password=user_form.cleaned_data['password']
            if(password != ""):
                user.set_password(password)
            else:
                user.password=oldPassword
            user.save()
            employee = employee_form.save(commit=False)
            employee.userId=user
            employee.save()
            messages.success(request,"El empleado se ha editado con exito")
            return redirect("/adminViews/listEmployee")
    else:
        user_form=userUpdateForm(instance=user)
        employee_form=employeeForm(instance=employee)
        
    return render(request,"adminApp/employee_form.html",{"user_form":user_form,"employee_form":employee_form})

@method_decorator([login_required,admin_required], name="dispatch")
class UsuarioDeleteView(SuccessMessageMixin,DeleteView):
    model=Usuario
    success_url="/adminViews/listEmployee"
    success_message = "El empleado se ha eliminado con exito"
    
    def delete(self,request,*args,**kwargs):
        messages.success(self.request, self.success_message)
        return super(UsuarioDeleteView,self).delete(request,*args,**kwargs)

@login_required
@admin_required
def activateOrDeactivate(request,pk):
    user=Usuario.objects.get(pk=pk)
    if(user.is_active):
        user.is_active=False
        messages.success(request,"El empleado ("+str(user.username)+") se ha desactivado")
    else:
        user.is_active=True
        messages.success(request,"El empleado ("+str(user.username)+") se ha activado")
    user.save()
    return redirect("/adminViews/listEmployee")