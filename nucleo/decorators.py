from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponse

from nucleo.models import Client, Employee, Proyect

#Custom decorator
def must_be_yours(func):
    def check_and_call(request, *args, **kwargs):
        #user = request.user
        #print user.id
        pk = kwargs["pk"]
        if request.user.is_client == True:
            client = Client.objects.get(pk=pk)
            if not (client.id == request.user.Client.id): 
                return HttpResponse("It is not yours ! You are not permitted !",
                            content_type="application/json", status=403)
            return func(request, *args, **kwargs)
        if request.user.is_employee == True:
            employee = Employee.objects.get(pk=pk)
            if not (employee.id == request.user.Employee.id): 
                return HttpResponse("It is not yours ! You are not permitted !",
                            content_type="application/json", status=403)
            return func(request, *args, **kwargs)
    return check_and_call

def check_proyect_owner(func):
    def check_and_call(request, *args, **kwargs):
        #user = request.user
        #print user.id
        pk = kwargs["pk"]
        proyect = Proyect.objects.get(pk=pk)
        if not (proyect.employeeId.id == request.user.Employee.id): 
            return HttpResponse("It is not yours ! You are not permitted !",
                        content_type="application/json", status=403)
        return func(request, *args, **kwargs)
    return check_and_call

def is_employee(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_employee,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def is_client(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_client,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator