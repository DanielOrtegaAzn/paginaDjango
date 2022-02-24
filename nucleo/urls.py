from django.contrib import admin
from django.urls import path
from nucleo import views

urlpatterns = [
    path('',views.inicio,name="inicio"),
    path('createClient',views.ClientCreateView.as_view(),name="createClient"),
    path('updateProfile/<int:pk>', views.clientUpdate, name = "updateProfile"),
    path("proyect/list", views.listProyect, name = "proyectList"),
    path("proyect/form", views.createProyect, name = "proyectForm"),
    path("proyect/update/<int:pk>", views.ProyectUpdate.as_view(), name = "proyectUpdate"),
    path("proyect/details/<int:pk>", views.ProyectDetails.as_view(), name = "proyectDetail"),
    path("proyect/delete/<int:pk>", views.ProyectDelete.as_view(), name = "proyectDelete"),
    path("proyect/client/list", views.clientParticipateList, name = "clientPartList"),
    path("proyect/employee/list", views.employeeParticipateList, name = "employeePartList"),
    path("proyect/alumnList/<int:pk>", views.showAlumn, name = "proyectAlumnList"),
    path("proyect/alumnList/asignRole/<int:pk>", views.asingRoleView, name = "participateRoleForm"),
    path("proyect/alumnList/alumnDetail/<int:pk>", views.clientDetails, name = "alumnDetail"),
    path("api/list/<int:pk>", views.ProyectsApiView.as_view(), name = "apiList"),
    path("api/login", views.CustomApiLogin.as_view(), name = "apiLogin"),
    # path("proyect/alumnList/<String:role>", views.searchAlumnByRol, name = "roleFilter"),
    path("proyect/endProyect/<int:pk>",views.endProyect,name="endProyect"),
]