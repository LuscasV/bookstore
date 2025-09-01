from rest_framework import serializers
from order.models import Order
from product.models.product import Product
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "active"]


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    # Mostra o username do usuário ao invés do ID
    user = serializers.StringRelatedField()  # isso retorna o __str__ do User, normalmente o username

    class Meta:
        model = Order
        fields = ["id", "user", "product"]
