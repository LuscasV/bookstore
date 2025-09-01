import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from order.factories import OrderFactory, UserFactory
from product.factories import ProductFactory


class TestOrderViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_list_orders(self):
        order = OrderFactory(user=self.user)
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_order(self):
        order = OrderFactory(user=self.user)
        url = reverse("order-detail", args=[order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        """Deve criar um novo pedido com produtos"""
        product = ProductFactory()
        url = reverse("order-list")
        data = {
            "product_ids": [product.id]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_order(self):
        """Deve atualizar os produtos de um pedido"""
        order = OrderFactory(user=self.user)
        product = ProductFactory()
        url = reverse("order-detail", args=[order.id])
        data = {
            "product_ids": [product.id]
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        """Deve deletar um pedido"""
        order = OrderFactory(user=self.user)
        url = reverse("order-detail", args=[order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
