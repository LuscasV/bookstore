import pytest
from django.contrib.auth.models import User
from product.models.product import Product
from order.models.order import Order
from order.serializers.order_serializer import OrderSerializer

@pytest.mark.django_db
def test_order_serializer():
    # cria um usuário
    user = User.objects.create_user(username="lucas", password="123456")

    # cria produtos (note que agora é title e não name)
    product1 = Product.objects.create(title="Notebook", price=3500, active=True)
    product2 = Product.objects.create(title="Mouse", price=150, active=True)

    # cria o pedido
    order = Order.objects.create(user=user)
    order.product.set([product1, product2])

    # serializa o pedido
    serializer = OrderSerializer(order)

    data = serializer.data

    # valida dados
    assert data["user"] == "lucas"
    assert len(data["product"]) == 2
    assert data["product"][0]["title"] == "Notebook"
    assert data["product"][1]["title"] == "Mouse"
