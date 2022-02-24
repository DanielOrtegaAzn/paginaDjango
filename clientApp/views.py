from asyncio.windows_events import NULL
import colorsys
from datetime import date, timedelta
import datetime
from enum import auto
from io import BytesIO
from turtle import pos
from typing import final
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView
from clientApp.forms import pdfForm
from nucleo.models import Category, Employee, Proyect, Client, Participate
from clientApp.decorators import client_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.platypus import TableStyle,Table
from reportlab.lib import colors

from registration.models import Usuario

'''class ProyectListView(ListView):
    model=Proyect'''
proyectosPDF=[]

@login_required
@client_required
def joinProyect(request,pk,week):
    proyecto=Proyect.objects.get(pk=pk)
    cliente=Client.objects.get(userId=request.user.pk)
    fecha=date.today()
    
    #Evitamos que puedan poner proyectos no disponibles (ya terminados)
    if(proyecto.endDate<fecha):
        messages.warning(request,"El proyecto "+str(proyecto.title)+" ya concluyo, no puedes inscribirte")
        return redirect("/clientViews/listProyect/0/"+str(week))
    
    #Evitamos que alguien se inscriba dos veces en el mismo cambiando la url
    for p in Participate.objects.all():
        if(proyecto.pk==p.proyectId.pk and cliente.pk==p.clientId.pk):
            messages.warning(request,"Ya estas inscrito en el proyecto "+str(proyecto.title))
            return redirect("/clientViews/listProyect/0/"+str(week))
    
    if(request.method == "POST"):
        participacion = Participate()
        participacion.proyectId=proyecto
        participacion.clientId=Client.objects.get(userId=request.user.pk)
        participacion.inscriptionDate=date.today()
        participacion.save()
        
        messages.success(request,"Inscripcion en "+str(proyecto.title)+" realizada con exito")
        return redirect("/clientViews/listProyect/0/"+str(week))
    
    return render(request,"clientApp/confirm_proyect.html",{"name":proyecto.title,"week":week})

@login_required
@client_required
def showProyects(request,categoryId,week):
    if(request.method=="GET"):
        categoryName=""
        proyectsList=[]
        proxSemana=NULL
        #Categoria
        if(categoryId==0):
            proyectos=Proyect.objects.all()
            categoryName="Todos"
        else:
            category=Category.objects.get(pk=categoryId)
            categoryName=category.name
            proyectos=Proyect.objects.filter(categoryId=category).all()
        
        #Filtrar solo proxima semana
        if(week==1):
            fecha2=date(2022,2,7)
            fecha=date.today()
            #Calculo los dias para llegar a la proxima semana
            dif=7-fecha.weekday()
            proxSemana=fecha+datetime.timedelta(days=dif)
            #Comparamos(lte=menor o igual)
            proyectos=proyectos.filter(startDate__gte=proxSemana, startDate__lte=proxSemana+datetime.timedelta(days=7))
        
        #Obtenemos el resto de datos
        cliente=Client.objects.get(userId=request.user.pk)
        participaciones=Participate.objects.filter(clientId=cliente.pk).all()
        categorias=Category.objects.all()
        
        #Quitamos los proyectos que no cumplan requerimientos de fecha
        for p in proyectos:
            if(p.isValid() or week==1):
                inscrito=False
                for pa in participaciones:
                    if(pa.proyectId.pk==p.pk):
                        inscrito=True
                proyectsList.append([p,inscrito])
        
        #Devolvemos la vista
        return render(request,"clientApp/proyect_list.html",{"proyect_list":proyectsList,"participate_list":participaciones,
                            "category_list":categorias,"category_name":categoryName,"week":week})

def obtenerProyectos(request,inicio,fin):
    global proyectosPDF
    #Pasamos los string a date
    inicioList=inicio.split("-")
    f1=date(int(inicioList[0]),int(inicioList[1]),int(inicioList[2]))
    finList=fin.split("-")
    f2=date(int(finList[0]),int(finList[1]),int(finList[2]))
    
    #Obtenemos el cliente y todas las participaciones
    cliente=Client.objects.get(userId=request.user)
    listaParticipaciones=Participate.objects.all()
    proyectos=[]
    #Obtenemos la fecha actual
    hoy=date.today()
    #Usamos las participaciones para encontrar los proyectos del cliente
    for participacion in listaParticipaciones:
        if(participacion.clientId==cliente):
            proyecto=Proyect.objects.get(pk=participacion.proyectId.pk)
            #Filtramos por fecha
            #(proyecto.startDate>=f1 and proyecto.endDate<=f2)
            if(proyecto.startDate>=f1 and proyecto.endDate<=f2):
                if(proyecto.endDate<hoy):
                    proyectos.append(proyecto)
    #Guardamos los proyectos en la variable global
    proyectosPDF=proyectos
    
class InformePDFCliente(View):
    global proyectosPDF
    
    def cabecera(self,pdf,user):
        cliente=Client.objects.get(userId=user)
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/logo.png'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True,mask='auto')
        #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica-Bold", 16)
        #Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(210, 790, u"INFORME CLIENTE:"+str(user.username.upper()))
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(215, 770, u"REPORTE DE PROYECTOS")
        pdf.drawString(40,730,u"Datos: ")
        pdf.setFont("Helvetica", 9)
        pdf.drawString(40,710,u"DNI: "+cliente.dni)
        pdf.drawString(40,695,u"Nombre y apellidos: "+cliente.name+" "+cliente.surname)
        pdf.drawString(40,680,u"Direccion: "+cliente.address)
        pdf.drawString(40,665,u"Fecha de nacimiento: "+str(cliente.address))
        pdf.drawString(40,650,u"Fecha de alta: "+str(cliente.fechaAlta))
    
    def tabla(self,pdf,proyect,y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Nivel', 'Fecha de inicio','Fecha de fin')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(proyect.level, proyect.startDate,proyect.endDate)]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        proyectos = Table([encabezados] + detalles, colWidths=[35,74,70])
        proyectos.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                #La fuente del encabezado
                ('FONT',(0,0), (-1,0), 'Helvetica-Bold')
            ]
        ))
        proyectos.wrapOn(pdf, 800, 600)
        proyectos.drawOn(pdf,40,y)
    
    #Para que el texto no se salga de la pagina
    def writeParagraph(self,pdf,dato,posicion,lineaInicial):
        descripcionProyecto=""
        cont=0
        lenAprox=75
        #Escribimos la linea inicial
        pdf.setFont("Helvetica-Bold",12)
        pdf.drawString(40,posicion,lineaInicial)
        pdf.setFont("Helvetica",11)
        #Bucle contando letras, simbolos y espacios
        for l in dato:
            #Si pasa al limite y es un espacio escribimos primera linea
            if(cont>lenAprox and l==" "):
                posicion-=16
                pdf.drawString(40,posicion,descripcionProyecto)
                cont=0
                descripcionProyecto=""
            #Añadimos el elemento al string
            else:
                descripcionProyecto+=l
                cont+=1
        #Añadimos la seccion de texto que quede
        if(cont != 0):
            posicion-=16
            pdf.drawString(40,posicion,descripcionProyecto)
        return posicion
                
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf,request.user)
        
        #Escribo los proyectos
        listaProyectos=proyectosPDF
        print(listaProyectos)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200,610,u"PROYECTOS DEL CLIENTE:")
        
        posicion=560
        numProyecto=1
        
        #Bucle para añadir proyectos
        for proyecto in listaProyectos:
            if(posicion<200):
                pdf.showPage()
                posicion=760
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(40,posicion,"Proyecto"+str(numProyecto)+": "+proyecto.title)
            numProyecto+=1
            posicion=posicion-60
            self.tabla(pdf,proyecto,posicion)
            
            posicion=posicion-30
            posicion=self.writeParagraph(pdf,proyecto.description,posicion,"Descripcion: ")
            posicion=posicion-20
            posicion=self.writeParagraph(pdf,proyecto.endingReport,posicion,"Reporte final: ")
            posicion=posicion-60
        
        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response