from rest_framework import serializers
from product.models import Product, Category
from product.serializers.category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "active", "category"]
