from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.factories import ProductFactory, CategoryFactory
from order.factories import UserFactory


class TestProductViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_list_products(self):
        product = ProductFactory()
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        product = ProductFactory()
        url = reverse("product-detail", args=[product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        category = CategoryFactory()
        url = reverse("product-list")
        data = {
            "title": "Notebook",
            "description": "Notebook potente",
            "price": 5000,
            "active": True,
            "category_ids": [category.id]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_product(self):
        product = ProductFactory()
        category = CategoryFactory()
        url = reverse("product-detail", args=[product.id])
        data = {
            "title": "Notebook Atualizado",
            "description": "Descrição nova",
            "price": 6000,
            "active": True,
            "category_ids": [category.id]
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        product = ProductFactory()
        url = reverse("product-detail", args=[product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
