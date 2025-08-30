from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer


class CategoryViewSet(ModelViewSet):
    """
    ViewSet para gerenciar categorias.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Category.objects.all().order_by("id")
