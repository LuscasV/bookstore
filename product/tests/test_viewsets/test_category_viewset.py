import json
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from product.factories import CategoryFactory
from order.factories import UserFactory

@pytest.mark.django_db
class TestCategoryViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        self.category = CategoryFactory(title="electronics")

    def test_get_all_category(self):
        url = reverse("category-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
    
        # Se o retorno é uma lista
        assert data[0]["title"] == self.category.title

    def test_create_category(self):
        self.user = UserFactory(is_staff=True)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        url = reverse("category-list")
        data = json.dumps({"title": "technology"})
        response = self.client.post(url, data=data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED
