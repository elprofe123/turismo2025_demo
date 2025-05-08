from django.db import models
from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)  # Nombre de la categoría
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional

    def __str__(self):
        return self.nombre  # Devuelve el nombre de la categoría



class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descripción = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    #important = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    imagen =  models.ImageField(upload_to='imagenes/', blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    categorias = models.ManyToManyField(Categoria, blank=True)

    def __str__(self):
        return self.titulo  # funcion que devuelve el titulo de la tarea y el usuario que la creo

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos adicionales para el perfil del usuario
    # Por ejemplo, puedes agregar un campo de imagen de perfil
    imagen = models.ImageField(upload_to='perfiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username  # Devuelve el nombre de usuario asociado al perfil



