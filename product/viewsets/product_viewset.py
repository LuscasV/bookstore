from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer


class ProductViewSet(ModelViewSet):
    """
    ViewSet para gerenciar produtos.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Product.objects.all().order_by("id")
