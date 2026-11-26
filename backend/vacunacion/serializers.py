from rest_framework import serializers
from .models import *
from accounts.models import *

class ScopedFieldsMixin:
    scoped_fields = {}  # {'nombre_campo': funcion_de_scope}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is None:
            return
        for name, scope in self.scoped_fields.items():
            field = self.fields.get(name)
            if field is not None and hasattr(field, 'queryset'):
                field.queryset = scope(request.user)

def ninos_visibles(user):
    if not user.is_authenticated:
        return Nino.objects.none()
    if user.rol == Usuario.Rol.SUPERVISOR:
        return Nino.objects.all()
    if user.rol == Usuario.Rol.PERSONAL_SALUD:
        personal = getattr(user, 'personal', None)
        if personal:
            return Nino.objects.filter(localidad_id=personal.localidad_id)
    if user.rol == Usuario.Rol.FAMILIAR:
        madre = getattr(user, 'madre', None)
        if madre:
            return Nino.objects.filter(madre=madre)
    return Nino.objects.none()

def madres_visibles(user):
    if not user.is_authenticated:
        return Madre.objects.none()
    if user.rol == Usuario.Rol.SUPERVISOR:
        return Madre.objects.all()
    if user.rol == Usuario.Rol.PERSONAL_SALUD:
        personal = getattr(user, 'personal', None)
        if personal:
            return Madre.objects.filter(localidad_id=personal.localidad_id)
    if user.rol == Usuario.Rol.FAMILIAR:
        madre = getattr(user, 'madre', None)
        if madre:
            return Madre.objects.filter(id=madre.id)
    return Madre.objects.none()

def localidades_visibles(user):
    if not user.is_authenticated:
        return Localidad.objects.none()
    if user.rol == Usuario.Rol.SUPERVISOR:
        return Localidad.objects.all()
    if user.rol == Usuario.Rol.PERSONAL_SALUD:
        personal = getattr(user, 'personal', None)
        if personal:
            return Localidad.objects.filter(id=personal.localidad_id)
    return Localidad.objects.none()

class VacunaSerializer(ScopedFieldsMixin,serializers.ModelSerializer):

    personal_nombre = serializers.CharField(source='personal.nombre',read_only=True)
    vacuna_nombre = serializers.CharField(source='tipo_vacuna.nombre',read_only=True)
    nino_nombre = serializers.CharField(source='nino.__str__', read_only=True)
    scoped_fields = {'nino': ninos_visibles}
    class Meta:
        model = Vacuna
        fields = [
            'id', 
            'nino_nombre',
            'nino',
            'tipo_vacuna',
            'vacuna_nombre',
            'fecha_aplicacion',
            'personal',
            'personal_nombre',
        ]
        read_only_fields = ['id','personal',]

class MadreSerializer(ScopedFieldsMixin,serializers.ModelSerializer):
    localidad_nombre = serializers.CharField(source='localidad.nombre',read_only=True)
    scoped_fields = {'localidad': localidades_visibles}
    class Meta:
        model = Madre
        fields = [
            'id', #read 
            'nombre',
            'cui',
            'fecha_nacimiento',
            'telefono',
            'localidad', 
            'localidad_nombre', #read
        ]
        read_only_fields = ['id',]

class TipoVacunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVacuna
        fields = [
            'id', #read 
            'nombre',
            'edad_recomendada_meses',
        ]
        read_only_fields = ['id',]

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = [
            'id', #read 
            'nombre',
            'municipio',
            'departamento',
        ]
        read_only_fields = ['id',]

class NinoSerializer(ScopedFieldsMixin, serializers.ModelSerializer):
    localidad_nombre = serializers.CharField(source='localidad.nombre',read_only=True)
    madre_nombre = serializers.CharField(source='madre.nombre',read_only=True)

    def validate_cui(self, value):
        if value == '':
            return None
        return value
    
    scoped_fields = {
        'localidad': localidades_visibles,
        'madre': madres_visibles,
    }
    class Meta:
        model = Nino 
        fields = [
            'id', #read 
            'nombre',
            'apellido',
            'cui',
            'fecha_nacimiento',
            'sexo',
            'localidad', 
            'localidad_nombre', #read
            'madre',
            'madre_nombre', #read
            'esquema_completo' #read
        ]
        read_only_fields = ['id','esquema_completo']

class PersonalSaludSerializer(serializers.ModelSerializer):
    localidad_nombre = serializers.CharField(source='localidad.nombre',read_only=True)
    class Meta:
        model = PersonalSalud
        fields = [
            'id', #read 
            'nombre',
            'profesion',
            'localidad',
            'localidad_nombre' #read
        ]
        read_only_fields = ['id',]


