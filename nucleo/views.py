from asyncio.windows_events import NULL
from datetime import date
from urllib.request import Request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from clientApp.forms import pdfForm
from clientApp import views
from nucleo.serializer import ProyectSerializer
from registration.forms import clientForm
from registration.models import Usuario

from nucleo.models import Client, Participate, Proyect

from nucleo.forms import ParticipateRoleForm, endProyectForm, userUpdateForm, clientUpdateForm, ProyectForm, ProyectUpdateForm

from nucleo.decorators import must_be_yours, check_proyect_owner, is_client, is_employee

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

def inicio(request):

    return render(request,"inicio.html")

class ClientCreateView(CreateView):
    model=Client
    fields=['dni','name','surname','address','birthday','userId']
    success_url="accounts/login"

@method_decorator(must_be_yours, name = 'dispatch')
class UpdateClientView(UpdateView):
    model = Client
    form_class=clientForm
    success_url = "/"

@must_be_yours
def clientUpdate(request, pk):
    
    client = Client.objects.get(pk = pk)
    user = get_object_or_404(Usuario, username = getattr(client, 'userId'))
    oldPassword = user.password

    if request.method =="POST":
        user_form=userUpdateForm(data=request.POST, instance = user)
        client_form=clientUpdateForm(data=request.POST, instance = client)
        if client_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            password=user_form.cleaned_data['password']
            print(oldPassword)
            print("contraseña nueva: "+ password)
            if(password != ""):
                user.set_password(password)
            else:
                user.password = oldPassword
            user.save()
            client = client_form.save(commit=False)
            client.userId=user
            client.save()
            return redirect("/")
    else:
        user_form=userUpdateForm(instance = user)
        client_form=clientUpdateForm(instance = client)
        
    return render(request, "nucleo/client_update.html", {"user_form" : user_form, "client_form" : client_form})

@method_decorator(login_required, name = "dispatch")
class ListProyect(ListView):
    model = Proyect

@login_required
@is_employee
def listProyect(request):
    
    proyectList = Proyect.objects.filter(employeeId = request.user.Employee)

    return render(request, "nucleo/proyect_list.html", {"proyect_list" : proyectList})

# class CreateProyect(CreateView):
#     model = Proyect
#     form_class = ProyectForm
#     success_url = "proyect/list"
    
@login_required
@is_employee
def createProyect(request):
    if request.method == "POST":
        proyect_form = ProyectForm(data=request.POST)
        if proyect_form.is_valid():
            proyect = proyect_form.save(commit=False)
            print(request.user.Employee)
            proyect.employeeId = request.user.Employee
            proyect.save()
            return redirect("/proyect/list")
    else:
        proyect_form = ProyectForm()
        
    return render(request, "nucleo/proyect_form.html", {"proyect_form":proyect_form})

@method_decorator(login_required, name = 'dispatch')
class ProyectDetails(DetailView):
    model = Proyect
    
@method_decorator([login_required, is_employee, check_proyect_owner], name = 'dispatch')
class ProyectUpdate(UpdateView):
    model = Proyect
    fields = ['title', 'description', 'level', 'startDate', 'endDate', 'categoryId']
    # form_class = ProyectUpdateForm
    success_url = "/proyect/list"
    
@method_decorator([login_required, is_employee, check_proyect_owner], name = 'dispatch')
class ProyectDelete(DeleteView):
    model = Proyect
    success_url = "/proyect/list"

@login_required
@is_client
def clientParticipateList(request):

    if request.method == "POST":
        pdf_form=pdfForm(request.POST)
        inicio=pdf_form['inicio'].value()
        fin=pdf_form['final'].value()
        views.obtenerProyectos(request,inicio,fin)
        return redirect("informe_pdf")
    else:
        pdf_form=pdfForm()
        
        participateList = Participate.objects.all()
        
        partList = []
        
        today = date.today()
        
        for data in participateList:
            if data.proyectId.endDate:
                if data.proyectId.endDate < today and data.clientId == request.user.Client:
                    partList.append(data)

    return render(request, "nucleo/participate_list.html", {"participateList" : partList,"pdf_form":pdf_form})

@login_required
@is_employee
def employeeParticipateList(request):

    proyectList = Proyect.objects.order_by('endDate')

    pryList = []

    today = date.today()

    for data in proyectList:
        if data.endDate:
            if data.endDate < today and data.employeeId == request.user.Employee:
                pryList.append(data)

    return render(request, "nucleo/proyect_list.html", {"proyect_list" : pryList})

@login_required
@is_employee
def showAlumn(request, pk):

    participateList = Participate.objects.filter(proyectId__id = pk)

    rol1List = []
    rol2List = []
    roleList = ["Participante", "Organizador"]

    for data in participateList:
        if data.role == roleList[0]:
            rol1List.append(data)
        elif data.role == roleList[1]:
            rol2List.append(data)

    # for data in proyectList:
    #     alumnList.append(data.clientId)

    return render(request, "nucleo/alumn_list.html", {"participateList" : participateList, "roleList" : roleList, "rol1List" : rol1List, "rol2List" : rol2List})

@login_required
@is_employee
def asingRoleView(request, pk):
    
    participate = Participate.objects.get(pk = pk)
    
    roleList = ["organizador", "participante"]
    
    if participate.proyectId.employeeId == request.user.Employee:
    
        if request.method == "POST":
            participateForm = ParticipateRoleForm(data=request.POST, instance = participate)
            if participateForm.is_valid():
                p = participateForm.save(commit=False)
                p.role = participateForm.cleaned_data['role']
                p.save()
                return redirect("/proyect/alumnList/"+str(participate.proyectId.id))
        else:
            participateForm=ParticipateRoleForm(instance = participate)
            
        return render(request, "nucleo/participateRoleForm.html", {"participateForm" : participateForm, "roleList" : roleList})
    else:
        return render(request, "nucleo/alumn_list.html", {"notYours" : "No puedes asignar roles en un proyecto ajeno"})

@login_required
@is_employee
def clientDetails(request, pk):

    client = Client.objects.get(pk = pk)

    return render(request, "nucleo/clientDetail.html", {"client" : client})

@login_required
@is_employee
def searchAlumnByRol(request, role):
    
    participateList = Participate.objects.filter(role = role)
            
    return render(request, "nucleo/alumn_list.html", {"participateList" : participateList})

@login_required
@is_employee
def endProyect(request,pk):
    proyect = Proyect.objects.get(pk=pk)
    
    #Para que no se puedan finalizar proyectos ya terminados y/o de otro empleado cambiando la url
    if(proyect.employeeId.userId.pk!=request.user.pk):
        messages.warning(request,"No dispones de este proyecto")
        return redirect("/proyect/list")
    elif(not proyect.isValid()):
        messages.warning(request,"El proyecto "+str(proyect.title)+" ya ha finalizado")
        return redirect("/proyect/list")
    
    if(request.method == "POST"):
        endProyect_form = endProyectForm(data=request.POST,instance=proyect)
        
        if(endProyect_form.is_valid()):
            proyect = endProyect_form.save(commit=False)
            
            if(proyect.endingReport):
                proyect.endDate=date.today()
                proyect.save()
                messages.success(request,"Proyecto "+str(proyect.title)+" finalizado con exito")
                return redirect("/proyect/list")
            else:
                messages.warning(request,"El reporte final no puede ser nulo")
    else:
        endProyect_form=endProyectForm(instance=proyect)
        
    return render(request,"nucleo/endProyect_form.html",{"endProyect_form":endProyect_form})

''' Vistas Apirest '''

class ProyectsApiView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        return Client.objects.get(pk = pk)
    
    def get(self, request, pk, format=None, *args, **kwargs):
        
        today = date.today()
        
        proyects = []
        
        participateList = Participate.objects.filter(clientId = self.get_object(pk))
        
        for data in participateList:
            if data.proyectId.endDate < today:
                proyects.append(data.proyectId)
        
        serializer = ProyectSerializer(proyects, many = True)
        
        return Response(serializer.data)

#No sirve
class loginTest(APIView):
    
    def get(self, request, format = None):
        return Response({'detail': 'GET Response'})
    
    def post(self, request, format = None):
        
        data = request.data
        
        if "user" not in data or "password" not in data:
            return Response(
                'wrong credentials',
                status = status.HTTP_401_UNAUTHORIZED
            )
            
        user = Usuario.objects.get(username = data["user"])
        if user.password == data["password"]:
            token = Token.objects.get_or_create(user = user)
            return Response({'detail': 'POST answer', 'token' : token[0].key})
        else:
            return Response(
                'Incorrect password',
                status = status.HTTP_401_UNAUTHORIZED
            )


class CustomApiLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data,
                                           context = {'request': request})
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        if(user.is_client):
            token, created = Token.objects.get_or_create(user = user)
            return Response({
                'token': token.key,
                'username': user.username,
                'name': user.Client.name,
                'surname': user.Client.surname,
            })
        else:
            return Response({
                'error': "Login user is not client",       
            })
        
    
