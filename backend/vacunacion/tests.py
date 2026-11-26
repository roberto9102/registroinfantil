from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Usuario

from .models import *


class LocalidadTests(APITestCase):

    def setUp(self):
        self.localidad = Localidad.objects.create(
            nombre="Localidad de prueba",
            municipio="Flores",
            departamento="Petén"
        )

        self.localidad2 = Localidad.objects.create(
                    nombre="Localidad de prueba",
                    municipio="Poptun",
                    departamento="Petén"
                )
        
        self.localidad3 = Localidad.objects.create(
                    nombre="Localidad de prueba",
                    municipio="Dolores",
                    departamento="Petén"
                )

        self.localidad4 = Localidad.objects.create(
                    nombre="Localidad de prueba",
                    municipio="Dolores",
                    departamento="Petén"
                )


        personal = PersonalSalud.objects.create(
            nombre="Supervisor de prueba",
            profesion=PersonalSalud.Profesion.MEDICO,
            localidad=self.localidad
        )

        familiar = Madre.objects.create(
            nombre="Maria Antonieta",
            cui="1234567890",
            fecha_nacimiento="2000-02-23",
            telefono="12345678",
            localidad=self.localidad
        )

        self.supervisor = Usuario.objects.create_user(
            username="supervisor_test",
            password="PruebaLocal123!",
            rol=Usuario.Rol.SUPERVISOR
        )

        self.personal = Usuario.objects.create_user(
            username="personal_test",
            password="PruebaLocal123!",
            rol=Usuario.Rol.PERSONAL_SALUD,
            personal=personal
        )

        self.familiar = Usuario.objects.create_user(
            username="familiar_test",
            password="PruebaLocal123!",
            rol=Usuario.Rol.FAMILIAR,
            madre=familiar
        )

    def test_supervisor_puede_listar_todos(self):
        self.client.force_authenticate(
            user=self.supervisor
        )

        response = self.client.get(
            '/api/localidades/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_personal_puede_listar_todos(self):
        self.client.force_authenticate(
            user=self.personal
        )

        response = self.client.get(
            '/api/localidades/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_familiar_no_puede_listar_todos(self):
        self.client.force_authenticate(
            user=self.familiar
        )

        response = self.client.get(
            '/api/localidades/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        
    def test_supervisor_puede_crear_localidad(self):

        self.client.force_authenticate(
            user=self.supervisor
        )

        datos = {
            'nombre': 'Nueva localidad',
            'municipio': 'Poptún',
            'departamento': 'Petén'
        }

        response = self.client.post(
            '/api/localidades/',
            datos,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Localidad.objects.filter(
                nombre='Nueva localidad'
            ).exists()
        )

    def test_personal_no_puede_crear_localidad(self):

        self.client.force_authenticate(
            user=self.personal
        )

        datos = {
            'nombre': 'Nueva localidad',
            'municipio': 'Poptún',
            'departamento': 'Petén'
        }

        response = self.client.post(
            '/api/localidades/',
            datos,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertFalse(
            Localidad.objects.filter(
                nombre='Nueva localidad'
            ).exists()
        )

    def test_familiar_no_puede_crear_localidad(self):
    
            self.client.force_authenticate(
                user=self.familiar
            )
    
            datos = {
                'nombre': 'Nueva localidad',
                'municipio': 'Poptún',
                'departamento': 'Petén'
            }
    
            response = self.client.post(
                '/api/localidades/',
                datos,
                format='json'
            )
    
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN
            )
    
            self.assertFalse(
                Localidad.objects.filter(
                    nombre='Nueva localidad'
                ).exists()
            )

    def test_supervisor_puede_borrar_localidad(self):
        self.client.force_authenticate(
            user=self.supervisor
        )

        response = self.client.delete(
            f'/api/localidades/{self.localidad4.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_personal_no_puede_borrar_localidad(self):
        self.client.force_authenticate(
            user=self.personal
        )

        response = self.client.delete(
            f'/api/localidades/{self.localidad3.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_familiar_no_puede_borrar_localidad(self):
        self.client.force_authenticate(
            user=self.familiar
        )

        response = self.client.delete(
            f'/api/localidades/{self.localidad3.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_supervisor_puede_actualizar_localidad(self):
        self.client.force_authenticate(
            user=self.supervisor
        )

        response = self.client.patch(
            f'/api/localidades/{self.localidad.id}/',
            {
            'nombre': 'Nuevo nombre'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_personal_no_puede_actualizar_localidad(self):
        self.client.force_authenticate(
            user=self.personal
        )

        response = self.client.patch(
            f'/api/localidades/{self.localidad.id}/',
            {
            'nombre': 'Nuevo nombre'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_familiar_no_puede_actualizar_localidad(self):
        self.client.force_authenticate(
            user=self.familiar
        )

        response = self.client.patch(
            f'/api/localidades/{self.localidad.id}/',
            {
            'nombre': 'Nuevo nombre'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

class MadreTests(APITestCase):
    pass 

class NinosTests(APITestCase):
    def setUp(self):
        self.localidad = Localidad.objects.create(
            nombre="Localidad de prueba",
            municipio="Flores",
            departamento="Petén"
        )

        self.localidad2 = Localidad.objects.create(
                    nombre="Localidad de prueba",
                    municipio="Poptun",
                    departamento="Petén"
                )

        self.personal = PersonalSalud.objects.create(
            nombre="Supervisor de prueba",
            profesion=PersonalSalud.Profesion.MEDICO,
            localidad=self.localidad
        )

        self.familiar = Madre.objects.create(
            nombre="Maria Antonieta",
            cui="1234567890",
            fecha_nacimiento="2000-02-23",
            telefono="12345678",
            localidad=self.localidad
        )

        self.supervisor_usuario = Usuario.objects.create_user(
            username="supervisor_test",
            password="PruebaLocal123!",
            rol=Usuario.Rol.SUPERVISOR
        )

        self.personal_usuario = Usuario.objects.create_user(
            username="personal_test",
            password="PruebaLocal123!",
            rol=Usuario.Rol.PERSONAL_SALUD,
            personal=self.personal
        )

        self.familiar_usuario = Usuario.objects.create_user(
            username="familiar_test",
            password="PruebaLocal123!",
            rol=Usuario.Rol.FAMILIAR,
            madre=self.familiar
        )    

        self.nino = Nino.objects.create(
            cui = "",
            nombre = "Maria",
            apellido="Del Carmen",
            fecha_nacimiento="2026-11-20",
            sexo = Nino.Sexo.FEMENINO,
            localidad=self.localidad,
            madre=self.familiar,
        )
        
        self.nino2 = Nino.objects.create(
            cui = "1",
            nombre = "Maria",
            apellido="Castellanos",
            fecha_nacimiento="2026-11-20",
            sexo = Nino.Sexo.FEMENINO,
            localidad=self.localidad2,
            madre=self.familiar,
        )

        self.nino3 = Nino.objects.create(
            cui = "2",
            nombre = "Maria",
            apellido="Castellanos",
            fecha_nacimiento="2026-11-20",
            sexo = Nino.Sexo.FEMENINO,
            localidad=self.localidad2,
            madre=self.familiar,
        )

    def test_supervisor_puede_crear_nino_y_con_cui_vacio(self):
        self.client.force_authenticate(
            user=self.supervisor_usuario
        )
        
        datos = {
            'cui' : "",
            'nombre' : "Carlos",
            'apellido' : "Del Carmen",
            'fecha_nacimiento' : "2026-11-20",
            'sexo' : Nino.Sexo.MASCULINO,
            'localidad' : self.localidad.id,
            'madre' : self.familiar.id,
        }

        datos2 = {
            'cui' : "",
            'nombre' : "Rayden",
            'apellido' : "Del Carmen",
            'fecha_nacimiento' : "2026-11-20",
            'sexo' : Nino.Sexo.MASCULINO,
            'localidad' : self.localidad2.id,
            'madre' : self.familiar.id,
        }

        datos3 = {
            'cui' : "123456",
            'nombre' : "Carlos",
            'apellido' : "Del Carmen",
            'fecha_nacimiento' : "2026-11-20",
            'sexo' : Nino.Sexo.MASCULINO,
            'localidad' : self.localidad.id,
            'madre' : self.familiar.id,
        }

        response = self.client.post(
            '/api/ninos/',
            datos,
            format="json"
        )

        response2 = self.client.post(
            '/api/ninos/',
            datos2,
            format="json"
        )

        response3 = self.client.post(
            '/api/ninos/',
            datos3,
            format="json"
        )
        

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response3.status_code,
            status.HTTP_201_CREATED
        )

        #self.assertIsNone(Nino.objects.get(id=self.nino.id).cui)

    def test_supervisor_no_puede_crear_nino_si_existe_cui(self):
        self.client.force_authenticate(
            user=self.supervisor_usuario
        )
        
        datos = {
            'cui' : "1",
            'nombre' : "Carlos",
            'apellido' : "Del Carmen",
            'fecha_nacimiento' : "2026-11-20",
            'sexo' : Nino.Sexo.MASCULINO,
            'localidad' : self.localidad.id,
            'madre' : self.familiar.id,
        }

        response = self.client.post(
            '/api/ninos/',
            datos,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_familiar_no_puede_crear_nino(self):
        self.client.force_authenticate(
            user=self.familiar_usuario
        )
        
        datos = {
            'cui' : "1",
            'nombre' : "Carlos",
            'apellido' : "Del Carmen",
            'fecha_nacimiento' : "2026-11-20",
            'sexo' : Nino.Sexo.MASCULINO,
            'localidad' : self.localidad.id,
            'madre' : self.familiar.id,
        }

        response = self.client.post(
            '/api/ninos/',
            datos,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_personal_puede_crear_nino_y_con_cui_vacio(self):
        self.client.force_authenticate(
            user=self.personal_usuario
        )
        
        datos = {
            'cui' : "",
            'nombre' : "Carlos",
            'apellido' : "Del Carmen",
            'fecha_nacimiento' : "2026-11-20",
            'sexo' : Nino.Sexo.MASCULINO,
            'localidad' : self.localidad.id,
            'madre' : self.familiar.id,
        }

        response = self.client.post(
            '/api/ninos/',
            datos,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
    
    def test_personal_no_puede_crear_otra_localidad(self):
        self.client.force_authenticate(
            user=self.personal_usuario
        )
        
        datos = {
            'cui' : "",
            'nombre' : "Carlos",
            'apellido' : "Del Carmen",
            'fecha_nacimiento' : "2026-11-20",
            'sexo' : Nino.Sexo.MASCULINO,
            'localidad' : self.localidad2.id,
            'madre' : self.familiar.id,
        }

        response = self.client.post(
            '/api/ninos/',
            datos,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_supervisor_puede_actualizar_nino(self):
        self.client.force_authenticate(
            user=self.supervisor_usuario
        )
        
        datos = {
            'cui' : "1",
            'nombre' : "Carlos",
            'apellido' : "Del Carmen",
            'fecha_nacimiento' : "2026-11-20",
            'sexo' : Nino.Sexo.MASCULINO,
            'localidad' : self.localidad.id,
            'madre' : self.familiar.id,
        }

        response = self.client.patch(
            f'/api/ninos/{self.nino2.id}/',
            {
                'nombre' : 'Sofia'
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    
    def test_familiar_no_puede_actualizar_nino(self):
        self.client.force_authenticate(
            user=self.familiar_usuario
        )

        response = self.client.patch(
            f'/api/ninos/{self.nino2.id}/',
            {
                'nombre' : 'Sofia'
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_personal_actualizar_misma_localidad(self):
        self.client.force_authenticate(
            user=self.personal_usuario
        )
        

        response = self.client.patch(
            f'/api/ninos/{self.nino.id}/',
            {
                'nombre' : 'Carlos'
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_personal_no_puede_actualizar_otra_localidad(self):
        self.client.force_authenticate(
            user=self.personal_usuario
        )
        

        response = self.client.patch(
            f'/api/ninos/{self.nino2.id}/',
            {
                'nombre' : 'Carlos'
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
    
    def test_supervisor_puede_eliminar(self):
        self.client.force_authenticate(
            user=self.supervisor_usuario
        )

        response = self.client.delete(
            f'/api/ninos/{self.nino3.id}/',
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_personal_no_puede_eliminar_otra_localidad(self):
        self.client.force_authenticate(
            user=self.personal_usuario
        )

        response = self.client.delete(
            f'/api/ninos/{self.nino.id}/',
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        response2 = self.client.delete(
            f'/api/ninos/{self.nino2.id}/',
            format="json"
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_404_NOT_FOUND
        )

class VacunasTests(APITestCase):
    def setUp(self):
        self.localidad = Localidad.objects.create(
            nombre="Localidad de prueba",
            municipio="Flores",
            departamento="Petén"
        )

        self.localidad2 = Localidad.objects.create(
                    nombre="Localidad de prueba",
                    municipio="Poptun",
                    departamento="Petén"
                )

        self.personal = PersonalSalud.objects.create(
            nombre="Maria Carla",
            profesion=PersonalSalud.Profesion.MEDICO,
            localidad=self.localidad
        )

        self.familiar = Madre.objects.create(
            nombre="Maria Antonieta",
            cui="1234567890",
            fecha_nacimiento="2000-02-23",
            telefono="12345678",
            localidad=self.localidad
        )

        self.familiar2 = Madre.objects.create(
            nombre="Maria Antonieta",
            cui="12345678901",
            fecha_nacimiento="2000-02-23",
            telefono="12345678",
            localidad=self.localidad2
        )

        self.supervisor_usuario = Usuario.objects.create_user(
            username="supervisor_test",
            password="PruebaLocal123!",
            rol=Usuario.Rol.SUPERVISOR
        )

        self.personal_usuario = Usuario.objects.create_user(
            username="personal_test",
            password="PruebaLocal123!",
            rol=Usuario.Rol.PERSONAL_SALUD,
            personal=self.personal
        )

        self.familiar_usuario = Usuario.objects.create_user(
            username="familiar_test",
            password="PruebaLocal123!",
            rol=Usuario.Rol.FAMILIAR,
            madre=self.familiar
        )    

        self.nino = Nino.objects.create(
            cui = "",
            nombre = "Maria",
            apellido="Del Carmen",
            fecha_nacimiento="2026-11-20",
            sexo = Nino.Sexo.FEMENINO,
            localidad=self.localidad,
            madre=self.familiar,
        )
        
        self.nino2 = Nino.objects.create(
            cui = "1",
            nombre = "Maria",
            apellido="Castellanos",
            fecha_nacimiento="2026-11-20",
            sexo = Nino.Sexo.FEMENINO,
            localidad=self.localidad2,
            madre=self.familiar2,
        )

        self.nino3 = Nino.objects.create(
            cui = "123",
            nombre = "Mari",
            apellido="Castellanos",
            fecha_nacimiento="2026-11-20",
            sexo = Nino.Sexo.FEMENINO,
            localidad=self.localidad,
            madre=self.familiar,
        )

        self.tipovacuna = TipoVacuna.objects.create(
            nombre = "Coronavirus",
            edad_recomendada_meses = "0"
        )

        self.tipovacuna2 = TipoVacuna.objects.create(
            nombre = "Viruela",
            edad_recomendada_meses = "2"
        )

        self.tipovacuna3 = TipoVacuna.objects.create(
            nombre = "Gripe",
            edad_recomendada_meses = "2"
        )

        self.vacuna = Vacuna.objects.create(
            nino = self.nino3,
            tipo_vacuna = self.tipovacuna3,
            personal = self.personal
        )

        self.vacuna2 = Vacuna.objects.create(
            nino = self.nino2,
            tipo_vacuna = self.tipovacuna3,
        )
    
    def test_supervisor_no_puede_crear_vacunas(self):
        self.client.force_authenticate(
            user=self.supervisor_usuario
        )
        
        datos = {
            'cui' : self.nino2.id,
            'tipo_vacuna' : self.tipovacuna.id,
        }

        response = self.client.post(
            '/api/vacunas/',
            datos,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_personal_puede_crear_vacunas_de_localidad_propia_y_no_de_otra(self):
        self.client.force_authenticate(
            user=self.personal_usuario
        )
        
        datos = {
            'nino' : self.nino.id,
            'tipo_vacuna' : self.tipovacuna2.id,
            
        }
        
        datos2 = {
            'nino' : self.nino2.id,
            'tipo_vacuna' : self.tipovacuna2.id,
        }

        response = self.client.post(
            '/api/vacunas/',
            datos,
            format="json"
        )
        
        response2 = self.client.post(
            '/api/vacunas/',
            datos2,
            format="json"
        )     

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(Vacuna.objects.get(nino=self.nino).personal, 
                        self.personal_usuario.personal)

    def test_familiar_solo_puede_listar_vacunas(self):
        self.client.force_authenticate(
            user=self.familiar_usuario
        )
        
        datos = {
            'nino' : self.nino.id,
            'tipo_vacuna' : self.tipovacuna2.id,
            
        }

        response = self.client.post(
            '/api/vacunas/',
            datos,
            format="json"
        )

        response2 = self.client.patch(
            f'/api/vacunas/{self.nino.id}/',
            {
            'nombre' : 'carlos'
            },
            format="json"
        )
        
        response3 = self.client.delete(
            f'/api/vacunas/{self.nino.id}/',
            format="json"
        )

        response4 = self.client.get(
            f'/api/vacunas/{self.vacuna.id}/',
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_403_FORBIDDEN
        )
        
        self.assertEqual(
            response3.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response4.status_code,
            status.HTTP_200_OK
        )

    def test_personal_solo_puede_actualizar_vacunas_propias(self):
        self.client.force_authenticate(
            user=self.personal_usuario
        )

        response = self.client.patch(
            f'/api/vacunas/{self.vacuna.id}/',
            {
                'tipo_vacuna' : self.tipovacuna2.id
            },
            format="json"
        )
        
        response2 = self.client.patch(
            f'/api/vacunas/{self.vacuna2.id}/',
            {
                'tipo_vacuna' : self.tipovacuna2.id
            },
            format="json"
        )     

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_404_NOT_FOUND
        )