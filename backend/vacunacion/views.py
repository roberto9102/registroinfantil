from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from accounts.permissions import *
from .models import *
from .serializers import *

#def get_queryset queryset.filter(self.request.user.madre) 
#puede ser declarado fuera del viewset pero es necesario llamar esa funcion desde una funcion propia del view definida getqueryset
class VacunaViewSet(viewsets.ModelViewSet):
    queryset = Vacuna.objects.select_related('tipo_vacuna','personal').all()
    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.rol == Usuario.Rol.SUPERVISOR : 
            return queryset
        elif user.rol == Usuario.Rol.FAMILIAR : 
            return queryset.filter(nino__madre = user.madre)     
        elif user.rol == Usuario.Rol.PERSONAL_SALUD : 
            return queryset
        else: 
            return queryset.none()
    serializer_class = VacunaSerializer
    permission_classes = [(EsFamiliar | EsSupervisor | EsPersonalSalud), CrearObjeto] 

class MadreViewSet(viewsets.ModelViewSet):
    queryset = Madre.objects.select_related('localidad').all()
    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.rol == Usuario.Rol.FAMILIAR : 
            return queryset.filter(nombre=user.madre.nombre)     
        elif user.rol in [Usuario.Rol.SUPERVISOR, Usuario.Rol.PERSONAL_SALUD] : 
                    return queryset
        else:
            return queryset.none()
    serializer_class = MadreSerializer
    permission_classes = [(EsSupervisor | EsPersonalSalud | EsFamiliar), CrearObjeto]

class NinoViewSet(viewsets.ModelViewSet):
    queryset = Nino.objects.select_related('madre','localidad').all()
    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.rol == Usuario.Rol.SUPERVISOR or user.rol == Usuario.Rol.PERSONAL_SALUD: 
            return queryset
        elif user.rol == Usuario.Rol.FAMILIAR : 
            return queryset.filter(madre=user.madre)     
        else:
            return queryset.none()
    serializer_class = NinoSerializer
    permission_classes = [(EsFamiliar | EsSupervisor | EsPersonalSalud), CrearObjeto] # | es importante para que lo tome como cualquiera

class TipoVacunaViewSet(viewsets.ModelViewSet):
    queryset = TipoVacuna.objects.all()
    serializer_class = TipoVacunaSerializer
    permission_classes = [EsSupervisor | EsPersonalSalud]

class LocalidadViewSet(viewsets.ModelViewSet):
    queryset = Localidad.objects.all()
    serializer_class = LocalidadSerializer
    permission_classes = [EsSupervisor | EsPersonalSalud]

class PersonalSaludViewSet(viewsets.ModelViewSet):
    queryset = PersonalSalud.objects.select_related('localidad').all()
    serializer_class = PersonalSaludSerializer
    permission_classes = [(EsSupervisor | EsPersonalSalud), CrearObjeto]