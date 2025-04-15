from django.db import models
from django.contrib.admin.models import LogEntry
from django.contrib import admin

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


    def __str__(self):
        return self.titulo  # funcion que devuelve el titulo de la tarea y el usuario que la creo



