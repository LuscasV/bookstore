import json
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from product.factories import ProductFactory, CategoryFactory
from product.models import Product
from order.factories import UserFactory

@pytest.mark.django_db
class TestProductViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        self.product = ProductFactory(title="pro controller", price=200.00)

    def test_get_all_product(self):
        url = reverse("product-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
        assert data[0]["title"] == self.product.title

    def test_create_product(self):
        self.user = UserFactory(is_staff=True)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        category = CategoryFactory()
        url = reverse("product-list")
        data = json.dumps({
            "title": "notebook",
            "price": 800.00,
            "categories_id": [category.id]
        })
        response = self.client.post(url, data=data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED
