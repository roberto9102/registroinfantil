from .models import Usuario
from rest_framework.permissions import BasePermission

class EsSupervisor(BasePermission):
    def has_permission(self, request, view):            
        return bool(request.user.is_authenticated and request.user.rol == Usuario.Rol.SUPERVISOR)

class EsFamiliar(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.rol == Usuario.Rol.FAMILIAR)

class EsPersonalSalud(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.rol == Usuario.Rol.PERSONAL_SALUD)

class PermisosMadre(BasePermission):
    def has_permission(self, request, view): 
        if view.action in ['list', 'retrieve']: 
            return True
        else:
            return request.user.rol in [Usuario.Rol.SUPERVISOR,Usuario.Rol.PERSONAL_SALUD] 

class PermisosNino(BasePermission):
    def has_permission(self, request, view): 
        if view.action in ['list', 'retrieve']:
            return True
        else:
            return request.user.rol in [Usuario.Rol.SUPERVISOR,Usuario.Rol.PERSONAL_SALUD]  #return true es en caso de cualquier otro metodo

class PermisosPersonal(BasePermission):
    def has_permission(self, request, view): 
        if view.action in ['list', 'retrieve']: 
            return True
        else:
            return request.user.rol in [Usuario.Rol.SUPERVISOR]  #return true es en caso de cualquier otro metodo

class PermisosVacuna(BasePermission):
    def has_permission(self, request, view): 
        if view.action in ['list', 'retrieve']: 
            return True
        elif view.action in ['update', 'partial_update']:
            return request.user.rol in [Usuario.Rol.PERSONAL_SALUD] 
        elif view.action in ['destroy']:
            return request.user.rol in [Usuario.Rol.SUPERVISOR] 
        else: #create
            return request.user.rol in [Usuario.Rol.PERSONAL_SALUD] 

class PermisosLocalidad(BasePermission):
    def has_permission(self, request, view): 
        if view.action in ['list', 'retrieve']: 
            return request.user.rol in [Usuario.Rol.SUPERVISOR, Usuario.Rol.PERSONAL_SALUD] 
        else: 
            return request.user.rol in [Usuario.Rol.SUPERVISOR] 

class PermisosTipoVacuna(BasePermission):
    def has_permission(self, request, view): 
        if view.action in ['list', 'retrieve']: 
            return True
        else: 
            return request.user.rol in [Usuario.Rol.SUPERVISOR, Usuario.Rol.PERSONAL_SALUD] 

class EditarVacuna(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.rol == Usuario.Rol.PERSONAL_SALUD and view.action in ['update','partial_update']:
            return(user.personal == obj.personal)
        else:
            return True