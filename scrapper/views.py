from rest_framework.generics import ListAPIView
from .models import Product, Brand
from .serializers import ProductSerializer, BrandSerializer
from rest_framework.response import Response


class ProductViewSet(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BrandProductListView(ListAPIView):
    def get(self, request, *args, **kwargs):
        # Fetch all brands and their related products in a single query
        brands = Brand.objects.prefetch_related('products').all()

        # Serialize the data using the BrandSerializer
        serializer = BrandSerializer(brands, many=True)

        # Return the serialized data as a response
        return Response(serializer.data)