from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from registration.models import Usuario

# Create your models here.

'''class User(models.Model):
    username = models.CharField(max_length = 40)
    password = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.username'''
    
class Employee(models.Model):
    dni = models.CharField(max_length = 9)
    name = models.CharField(max_length = 40)
    surname = models.CharField(max_length = 60)
    address = models.CharField(max_length = 150)
    biography = models.CharField(max_length = 255)
    userId = models.OneToOneField(Usuario, on_delete=models.CASCADE, verbose_name = "User", related_name = "Employee")
    #models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "User", related_name = "Employee")
    
    def __str__(self):
        return self.name + " " + self.surname
    
class Client(models.Model):
    dni = models.CharField(max_length = 9)
    name = models.CharField(max_length = 40)
    surname = models.CharField(max_length = 60)
    address = models.CharField(max_length = 150)
    birthday = models.DateField()
    fechaAlta = models.DateField(auto_now_add = True)
    userId = models.OneToOneField(Usuario, on_delete=models.CASCADE, verbose_name = "User", related_name = "Client")
    #models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "User", related_name = "Client")
    
    def __str__(self):
        return self.name + " " + self.surname
    
class Category(models.Model):
    name = models.CharField(max_length = 150)
    photo = models.ImageField(upload_to = "Photo", null = True, blank = True)
    
    
    def __str__(self):
        return self.name
    
class Proyect(models.Model):
    title = models.CharField(max_length = 150)
    description = models.CharField(max_length = 255)
    level = models.IntegerField()
    startDate = models.DateField()
    endDate = models.DateField(null=True,blank=True)
    endingReport = models.CharField(null=True, blank=True, max_length = 255)
    employeeId = ForeignKey(Employee, on_delete = models.CASCADE, related_name = "employee", verbose_name = "employee")
    categoryId = ForeignKey(Category, on_delete = models.CASCADE, related_name = "category", verbose_name = "category")
    
    def __str__(self):
        return self.title
    
    def isValid(self):
        if(not self.endDate or self.endDate>date.today()):
            return True
        else:
            return False
    
    def clientIsInProyect(self,user,participate):
        client=Client.objects.get(userId=user.pk)
        if(participate.clientId==client.pk):
            return True
        else:
            return False
    
class Participate(models.Model):
    
    roles = (
        ('Organizador', ('Organizador del proyecto')), 
        ('Participante', ('Participante del evento'))
    )
    
    clientId = models.ForeignKey(Client, on_delete = models.CASCADE, related_name = "client", verbose_name = "client")
    proyectId = models.ForeignKey(Proyect, on_delete = models.CASCADE, related_name = "proyect", verbose_name = "proyect")
    inscriptionDate = models.DateField(auto_now_add = True)
    role = models.CharField(max_length = 100, choices = roles, default = 'Participante')

    # def __str__(self):
    #     return self.clientId + "-" + self.proyectId.name
