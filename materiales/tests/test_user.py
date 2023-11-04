from django.test import TestCase

import json

from rest_framework.test import APIClient
from rest_framework import status

from materiales.models import (
    Autor,
    Genero,
    Carrera,
    Editorial,
    TipoMaterial,
    EstadoEjemplar,
    Material,
    Ejemplar,
)

from accounts.models import User


class User_MaterialTest(TestCase):
    @classmethod
    def setUp(self):
        user = User(
            username='ismael',
            email='ismael@mail.com'
        )
        user.set_password('Ñ>123`fr~')
        user.save()

        client = APIClient()
        response = client.post('/account/login/', {
            'email': 'ismael@mail.com',
            'password': 'Ñ>123`fr~',
        },
            format='json'
        )
        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user

    def test_create_material(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token' + self.access_token)

        # creamos los campos del material, Autor, Genero, Tipo, etc...        
        test_material1 = {
            'nombre': 'jasdfas',
        }

        response = client.post('/api/Autor/', test_material1, format='json')
        print(response)

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('pk', result)
        self.assertIn('nombre', result)

        if 'pk' in result:
            del result['pk']

        self.assertEqual(result, test_material1)


'''
        test_material = Material.objects.create(
            titulo='El mago',
            descripcion='La historia del 10, el potrero',
        )
        tipoMaterial = TipoMaterial.objects.all()
        editorialMaterial = Editorial.objects.all()
        autorMaterial = Autor.objects.all()
        carreraMaterial = Carrera.objects.all()
        generoMaterial = Genero.objects.all()

        test_material.tipo.set(tipoMaterial)
        test_material.editorial.set(editorialMaterial)
        test_material.autor.set(autorMaterial)
        test_material.carrera.set(carreraMaterial)
        test_material.genero.set(generoMaterial)
'''
