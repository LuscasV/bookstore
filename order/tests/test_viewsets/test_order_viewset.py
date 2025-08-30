import json
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from order.factories import UserFactory, OrderFactory
from product.factories import ProductFactory

@pytest.mark.django_db
class TestOrderViewSet:

    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        self.product = ProductFactory()
        self.order = OrderFactory(user=self.user)
        self.order.product = self.product
        self.order.save()

    def test_get_orders(self):
        url = reverse("order-list")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
        assert len(data) >= 1
        assert data["results"][0]["user"] == self.user.id

    def test_create_order(self):
        url = reverse("order-list")
        data = json.dumps({
            "user": self.user.id,
            "products_id": [self.product.id]
        })
        response = self.client.post(url, data=data, content_type="application/json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"] == self.user.id
