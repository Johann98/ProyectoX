from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

#General Models

class User(AbstractUser):
    pass
    #role = models.CharField(max_length=100)



class Proyecto(models.Model):
    titulo = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=500)
    arquitecto_id = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name_plural = "Proyectos"
        ordering = ['-id']

class Tarea(models.Model):
    titulo = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=500)
    avance = models.PositiveIntegerField(default=0)
    desarrolladores = models.TextField()
    estados = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    proyecto = models.ForeignKey(
        Proyecto,
        related_name='tarea',
        on_delete = models.CASCADE,
        null = False
    )
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name_plural = "Tareas"
        ordering = ['-id']
