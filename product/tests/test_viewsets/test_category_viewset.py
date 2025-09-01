from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.factories import CategoryFactory
from order.factories import UserFactory


class TestCategoryViewSet(APITestCase):
    def setUp(self):
        # Usuário staff para criar, atualizar e deletar categorias
        self.user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_list_categories(self):
        category = CategoryFactory()
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category(self):
        category = CategoryFactory()
        url = reverse("category-detail", args=[category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        url = reverse("category-list")
        data = {
            "title": "Tecnologia",
            "slug": "tecnologia",
            "description": "Categoria de tecnologia",
            "active": True
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category(self):
        category = CategoryFactory()
        url = reverse("category-detail", args=[category.id])
        data = {
            "title": "Tecnologia Atualizada",
            "slug": "tecnologia-atualizada",
            "description": "Descrição nova",
            "active": True
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        category = CategoryFactory()
        url = reverse("category-detail", args=[category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
