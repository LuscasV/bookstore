from rest_framework import serializers
from product.models import Product, Category
from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    # Detalhes completos das categorias no GET
    category = CategorySerializer(many=True, read_only=True)

    # Aceita IDs de categorias para POST/PUT
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        many=True,
        source="category"
    )

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "active", "category", "category_ids"]
