import pytest
from product.models import Category
from product.serializers.category_serializer import CategorySerializer

@pytest.mark.django_db
class TestCategorySerializer:
    def test_category_serializer_fields(self):
        category = Category.objects.create(
            title="Food",
            slug="food",
            description="Category for food items",
            active=True,
        )
        serializer = CategorySerializer(category)
        data = serializer.data

        assert set(data.keys()) == {"id", "title", "slug", "description", "active"}
        assert data["title"] == "Food"
        assert data["slug"] == "food"
        assert data["description"] == "Category for food items"
        assert data["active"] is True
