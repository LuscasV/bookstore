import pytest
from product.models import Product, Category
from product.serializers.product_serializer import ProductSerializer

@pytest.mark.django_db
class TestProductSerializer:
    def test_product_serializer_fields(self):
        category = Category.objects.create(
            title="Electronics",
            slug="electronics",
            description="Electronic items",
            active=True,
        )

        product = Product.objects.create(
            title="Smartphone",
            description="Latest smartphone model",
            price=1500,
            active=True,
        )
        product.category.add(category)

        serializer = ProductSerializer(product)
        data = serializer.data

        assert set(data.keys()) == {"id", "title", "description", "price", "active", "category"}
        assert data["title"] == "Smartphone"
        assert data["description"] == "Latest smartphone model"
        assert data["price"] == 1500
        assert data["active"] is True
        assert len(data["category"]) == 1
        assert data["category"][0]["title"] == "Electronics"
