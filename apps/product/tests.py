from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from PIL import Image
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product


class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_login(self.user)

    def test_get_product(self):
        product = Product.objects.create(
            name='Producto existente', description='Descripción existente', price=20.0, stock=50)
        url = reverse('get-detail', kwargs={'pk': product.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Producto existente')

    def test_create_product(self):
        url = reverse('create-list')
        data = {
            'name': 'Producto de prueba',
            'description': 'Descripción de prueba',
            'price': 100,
            'stock': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Producto de prueba')

    def test_wrong_product(self):
        url = reverse('create-list')
        data = {
            'name': 'ijabsdhbasjkhdbasd98q12318731t687#$%/!@#%41aijskbdasjkhbdasjhvbasjgdvahjgsvdhgavsdhgavsdhjgavsdhagvs1',
            'description': 'Descripción de prueba',
            'price': 12,
            'stock': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(
            response.data['name'][0], 'Ensure this field has no more than 100 characters.')

    def test_update_product(self):
        product = Product.objects.create(
            name='Producto existente', description='Descripción existente', price=20.0, stock=50)
        url = reverse('update-detail', kwargs={'pk': product.pk})
        data = {
            'name': 'Producto actualizado',
            'description': 'Descripción actualizada',
            'price': 30.0,
            'stock': 70
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(
            pk=product.pk).name, 'Producto actualizado')

    def test_delete_product(self):
        product = Product.objects.create(
            name='Producto a eliminar', description='Descripción a eliminar', price=15.0, stock=80)
        url = reverse('delete-detail', kwargs={'pk': product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_authentication_required(self):
        url = reverse('create-list')
        data = {
            'name': 'Producto de prueba',
            'description': 'Descripción de prueba',
            'price': 100,
            'stock': 100
        }
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_with_image(self):
        url = reverse('create-list')

        image = Image.new('RGB', (100, 100))
        image_file = BytesIO()
        image.save(image_file, 'JPEG')
        image_file.seek(0)

        image = SimpleUploadedFile(
            "test_image.jpg", image_file.read(), content_type="image/jpeg")

        data = {
            'name': 'Producto de prueba',
            'description': 'Descripción de prueba',
            'price': 100,
            'stock': 100,
            'image': image
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Producto de prueba')
        self.assertIsNotNone(Product.objects.get().image)
