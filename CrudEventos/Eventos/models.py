from django.db import models
from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descripción = models.TextField(blank=True)
    #imagen=models.ImageField(upload_to=None)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    #important = models.BooleanField(default=False)
    # Se relaciona con una tabla user proporcionada por django
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #cuando se elimine la tabla usuario se eliminara tambien sus tareas-- eliminacion cascada
    checked = models.BooleanField(default=False)
    imagen =  models.ImageField(upload_to='imagenes/', blank=True, null=True)

    def __str__(self):
        return self.titulo  # funcion que devuelve el titulo de la tarea y el usuario que la creo

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos adicionales para el perfil del usuario
    # Por ejemplo, puedes agregar un campo de imagen de perfil
    imagen = models.ImageField(upload_to='perfiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username  # Devuelve el nombre de usuario asociado al perfil

   
