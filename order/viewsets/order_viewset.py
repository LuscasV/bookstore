# order/viewsets.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from order.models import Order
from order.serializers.order_serializer import OrderSerializer
from product.models import Product

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada: usuários só podem alterar/deletar seus próprios pedidos.
    """

    def has_object_permission(self, request, view, obj):
        # Sempre permite métodos "seguros" (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Só permite alteração se o usuário for dono do pedido
        return obj.user == request.user


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Ao criar, o usuário logado é associado automaticamente.
        Permite criar pedidos com vários produtos.
        """
        products_ids = self.request.data.get("product", [])
        order = serializer.save(user=self.request.user)
        if products_ids:
            products = Product.objects.filter(id__in=products_ids)
            order.product.set(products)

    def perform_update(self, serializer):
        """
        Atualiza os produtos do pedido.
        """
        products_ids = self.request.data.get("product", [])
        order = serializer.save()
        if products_ids:
            products = Product.objects.filter(id__in=products_ids)
            order.product.set(products)
