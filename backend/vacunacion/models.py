from django.db import models

# Create your models here.
class TipoVacuna(models.Model):
    nombre = models.CharField(max_length=100)
    edad_recomendada_meses = models.PositiveIntegerField()
    def __str__(self):
        return self.nombre


class Localidad(models.Model):
    nombre = models.CharField(max_length=70)
    municipio = models.CharField(max_length=70)
    departamento = models.CharField(max_length=70)
    def __str__(self):
        return f"{self.nombre} - {self.municipio}"

class Madre(models.Model):
    nombre = models.CharField(max_length=150)
    cui = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(null=True, blank=True, max_length=8)
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT)
    def __str__(self):
        return self.nombre

class Nino(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = 'masculino'
        FEMENINO = 'femenino'

    cui = models.CharField(max_length=20, null=True, unique=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(choices=Sexo.choices, max_length=20)
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT)
    madre = models.ForeignKey(Madre, on_delete=models.PROTECT)
    esquema_completo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre}"

class PersonalSalud(models.Model):
    class Profesion(models.TextChoices):
        ENFERMERO = 'enfermero'
        MEDICO = 'medico'
    nombre = models.CharField(max_length=150)
    profesion = models.CharField(choices=Profesion.choices, max_length=40)
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.nombre} ({self.profesion})"

class Vacuna(models.Model):
    nino = models.ForeignKey(Nino, on_delete=models.PROTECT)
    fecha_aplicacion = models.DateTimeField(auto_now_add=True)
    tipo_vacuna = models.ForeignKey(TipoVacuna, on_delete=models.PROTECT)
    personal = models.ForeignKey(PersonalSalud,  on_delete=models.PROTECT, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nino', 'tipo_vacuna'],
                name='vacuna_unica_por_nino'
            )
        ]

    def __str__(self):
        return f"{self.tipo_vacuna.nombre} - {self.nino.nombre} "
    
