# order/tests/test_serializers.py
import pytest
from django.contrib.auth.models import User
from product.models import Product
from order.models import Order
from order.serializers import OrderSerializer

@pytest.mark.django_db
def test_order_serializer():
    # cria usuário
    user = User.objects.create_user(username="lucas", password="123456")

    # cria produtos
    product1 = Product.objects.create(name="Notebook", price=3500.00)
    product2 = Product.objects.create(name="Mouse", price=150.00)

    # cria ordem
    order = Order.objects.create(user=user)
    order.product.add(product1, product2)

    # serializa
    serializer = OrderSerializer(order)
    data = serializer.data

    # checagens
    assert data["user"] == "lucas"
    assert len(data["product"]) == 2
    assert any(p["name"] == "Notebook" for p in data["product"])
    assert any(p["name"] == "Mouse" for p in data["product"])
