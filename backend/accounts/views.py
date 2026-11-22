from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .permissions import *
from .models import Usuario
from .serializers import UsuarioSerializer
# Create your views here.

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.select_related('personal','madre').all()
    serializer_class = UsuarioSerializer

    permission_classes = [EsSupervisor]