from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('vacunas',VacunaViewSet, 'vacunas')
router.register('madres',MadreViewSet, 'madres')
router.register('tipovacunas',TipoVacunaViewSet, 'tipovacunas')
router.register('localidades',LocalidadViewSet, 'localidades')
router.register('personalsalud',PersonalSaludViewSet, 'personalsalud')
router.register('ninos',NinoViewSet, 'ninos')
urlpatterns = router.urls