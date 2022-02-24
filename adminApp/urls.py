from django.urls import path
from adminApp import views

urlpatterns = [
    path('listEmployee',views.EmployeeListView.as_view(),name="listEmployee"),
    path('createEmployee',views.employee,name="createEmployee"),
    path('updateEmployee/<int:pk>',views.updateEmployee,name="updateEmployee"),
    path('deleteUsuario/<int:pk>',views.UsuarioDeleteView.as_view(),name="deleteUsuario"),
    path('changeUser/<int:pk>',views.activateOrDeactivate,name="changeUser")
]
