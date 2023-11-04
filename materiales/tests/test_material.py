from django.test import TestCase

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
# Create all elements for add to Material


class AutorModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Autor.objects.create(nombre="Topo Yiyo")

    def test_Autor_name(self):
        autor = Autor.objects.get(id=1)
        field_label = autor.__getattribute__('nombre')
        self.assertEquals(field_label, 'nombre')

    def get_absolute_url(self):
        autor = Autor.objects.get(id=1)
        self.assertEqual(autor.get_absolute_url(), '/api/Autor/1')


class GeneroModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Genero.objects.create(nombre="Relato")

    def get_absolute_url(self):
        genero = Genero.objects.get(id=1)
        self.assertEqual(genero.get_absolute_url(), '/api/Genero/1')


class CarreraModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Carrera.objects.create(nombre="Taller")

    def get_absolute_url(self):
        carrera = Carrera.objects.get(id=1)
        self.assertEqual(carrera.get_absolute_url(),
                         '/api/Carrera/1')


class EditorialModelTest(TestCase):
    @classmethod
    def setUp(cls):
        editorial = Editorial.objects.create(nombre="FPT")

    def get_absolute_url(self):
        editorial = Editorial.objects.get(id=1)
        self.assertEqual(editorial.get_absolute_url(),
                         '/api/Editorial/1')


class TipoMaterialTest(TestCase):
    @classmethod
    def setUp(cls):
        TipoMaterial.objects.create(nombre="Audio/Video")

    def get_absolute_url(self):
        tipo = TipoMaterial.objects.get(id=1)
        self.assertEqual(tipo.objects.get_absolute_url(),
                         '/api/Tipo/1')


class EstadoEjemplarTest(TestCase):
    @classmethod
    def setUp(cls):
        estado = EstadoEjemplar.objects.create(nombre="Disponible")

    def get_absolute_url(self):
        estado = EstadoEjemplar.objects.get(id=1)
        self.assertEquals(EstadoEjemplar.objects.get_absolute_url(),
                          '/api/EstadoEjemplar/1')


#   Here we're insert elements in the class Materiales

class MaterialTest(TestCase):
    @classmethod
    def setUp(cls):

        material = Material.objects.create(
            titulo='El mago',
            descripcion='La historia del 10, el potrero',
        )
        tipoMaterial = TipoMaterial.objects.all()
        editorialMaterial = Editorial.objects.all()
        autorMaterial = Autor.objects.all()
        carreraMaterial = Carrera.objects.all()
        generoMaterial = Genero.objects.all()

        material.tipo.set(tipoMaterial)
        material.editorial.set(editorialMaterial)
        material.autor.set(autorMaterial)
        material.carrera.set(carreraMaterial)
        material.genero.set(generoMaterial)

        material.save()

    def test_Material_name(self):
        material = Material.objects.get(id=1)
        field_label = material.__getattribute__('titulo')
        self.assertEquals(field_label, 'El mago')

    def get_absolute_url(self):
        material = Material.objects.get(id=1)
        self.assertEquals(Material.objects.get_absolute_url(),
                          '/api/Material/1')
        print(self)
