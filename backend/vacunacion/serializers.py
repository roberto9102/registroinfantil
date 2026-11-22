from rest_framework import serializers
from .models import *

class VacunaSerializer(serializers.ModelSerializer):

    personal_nombre = serializers.CharField(source='personal.nombre',read_only=True)
    vacuna_nombre = serializers.CharField(source='tipo_vacuna.nombre',read_only=True)
    nino_nombre = serializers.CharField(source='nino.__str__', read_only=True)
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

class MadreSerializer(serializers.ModelSerializer):
    localidad_nombre = serializers.CharField(source='localidad.nombre',read_only=True)
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

class NinoSerializer(serializers.ModelSerializer):
    localidad_nombre = serializers.CharField(source='localidad.nombre',read_only=True)
    madre_nombre = serializers.CharField(source='madre.nombre',read_only=True)
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