from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        SUPERVISOR = 'supervisor'
        PERSONAL_SALUD = 'personal de salud'
        FAMILIAR = 'familiar'
    rol = models.CharField(choices=Rol.choices, max_length=20)

    personal = models.OneToOneField('vacunacion.PersonalSalud', on_delete=models.PROTECT, null=True, blank=True, related_name='usuario' )
    madre = models.OneToOneField('vacunacion.Madre', on_delete=models.PROTECT, null=True, blank=True, related_name='usuario')
