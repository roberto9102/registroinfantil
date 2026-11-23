from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from accounts.permissions import *
from .models import *
from .serializers import *

#def get_queryset queryset.filter(self.request.user.madre) 
#puede ser declarado fuera del viewset pero es necesario llamar esa funcion desde una funcion propia del view definida getqueryset
class VacunaViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Vacuna.objects.select_related('tipo_vacuna','personal','nino').all()
        user = self.request.user
        if user.rol == Usuario.Rol.SUPERVISOR : 
            return queryset
        elif user.rol == Usuario.Rol.FAMILIAR : 
            return queryset.filter(nino__madre = user.madre)     
        elif user.rol == Usuario.Rol.PERSONAL_SALUD : 
            return queryset.filter(localidad=user.personal.localidad)
        else: 
            return queryset.none()

    serializer_class = VacunaSerializer
    permission_classes = [(EsFamiliar | EsSupervisor | EsPersonalSalud), PermisosVacuna, EditarVacuna]

    def perform_create(self, serializer):
        user = self.request.user
        if user.rol == Usuario.Rol.PERSONAL_SALUD:
            serializer.save(personal=user.personal)
        else:
            serializer.save()

""" No sirve de nada en verdad ya que ya esta el editar vacunas y el read only
    def perform_update(self, serializer):
        user = self.request.user
        if user.rol == Usuario.Rol.PERSONAL_SALUD:
            serializer.save(personal=user.personal)
        else:
            serializer.save()
"""

class MadreViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Madre.objects.select_related('localidad').all()
        user = self.request.user
        if user.rol == Usuario.Rol.FAMILIAR : 
            return queryset.filter(id=user.madre.id)     
        elif user.rol == Usuario.Rol.SUPERVISOR : 
            return queryset
        elif user.rol == Usuario.Rol.PERSONAL_SALUD:
            return queryset.filter(localidad=user.personal.localidad)
        else:
            return queryset.none()
    serializer_class = MadreSerializer
    permission_classes = [(EsSupervisor | EsPersonalSalud | EsFamiliar), PermisosMadre]

class NinoViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Nino.objects.select_related('madre','localidad').all()
        user = self.request.user
        if user.rol == Usuario.Rol.SUPERVISOR: 
            return queryset
        elif user.rol == Usuario.Rol.PERSONAL_SALUD:
            return queryset.filter(localidad=user.personal.localidad)
        elif user.rol == Usuario.Rol.FAMILIAR : 
            return queryset.filter(madre=user.madre)     
        else:
            return queryset.none()
    serializer_class = NinoSerializer
    permission_classes = [(EsFamiliar | EsSupervisor | EsPersonalSalud), PermisosNino] # | es importante para que lo tome como cualquiera

class TipoVacunaViewSet(viewsets.ModelViewSet):
    queryset = TipoVacuna.objects.all()
    serializer_class = TipoVacunaSerializer
    permission_classes = [(EsSupervisor | EsPersonalSalud), PermisosTipoVacuna]

class LocalidadViewSet(viewsets.ModelViewSet):
    queryset = Localidad.objects.all()
    serializer_class = LocalidadSerializer
    permission_classes = [(EsSupervisor | EsPersonalSalud), PermisosLocalidad]

class PersonalSaludViewSet(viewsets.ModelViewSet):
    queryset = PersonalSalud.objects.select_related('localidad').all()
    serializer_class = PersonalSaludSerializer
    permission_classes = [(EsSupervisor | EsPersonalSalud), PermisosPersonal ]