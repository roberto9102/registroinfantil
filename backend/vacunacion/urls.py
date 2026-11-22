from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('vacunas',VacunaViewSet, 'vacunas')
router.register('madres',MadreViewSet, 'madres')
router.register('tipovacuna',TipoVacunaViewSet, 'tipovacuna')
router.register('localidad',LocalidadViewSet, 'localidad')
router.register('personalsalud',PersonalSaludViewSet, 'personalsalud')
router.register('nino',NinoViewSet, 'nino')
urlpatterns = router.urls