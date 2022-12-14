from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from api.products.serializers import ProductSerializer, CategorySerializer
from products.models import Category, Product
from products.filters import ProductFilter


class ProductsViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ProductFilter


class CategoriesViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='products',
            serializer_class=ProductSerializer)
    def get_products(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object().product_set,
                                         many=True)
        return Response(serializer.data)
