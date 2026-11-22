from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('vacunas',VacunaViewSet, 'vacunas')
router.register('madres',MadreViewSet, 'madres')
router.register('tipoVacuna',TipoVacunaViewSet, 'tipoVacuna')
router.register('localidad',LocalidadViewSet, 'localidad')
router.register('personalSalud',PersonalSaludViewSet, 'personalSalud')
router.register('nino',NinoViewSet, 'nino')
urlpatterns = router.urls