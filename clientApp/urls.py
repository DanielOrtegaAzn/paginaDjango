from django.urls import path
from clientApp import views

urlpatterns = [
    path('listProyect/<int:categoryId>/<int:week>',views.showProyects,name="listProyect"),
    #path('listProyect',views.ProyectListView.as_view(),name="listProyect"),
    path('confirmProyect/<int:pk>/<int:week>',views.joinProyect,name="confirmProyect"),
    path('informe_pdf',views.InformePDFCliente.as_view(),name="informe_pdf"),
]