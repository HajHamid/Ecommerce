
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from products.models import Brand
from products.serializers import BrandSerializer
from products.selectors import get_active_brands
from products.services import create_brand, update_brand


class BrandListView(APIView):
    def get(self, request):
        brands = get_active_brands()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class BrandCreateView(APIView):
    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_brand(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BrandUpdateView(APIView):
    def put(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response({'detail': 'brand not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BrandSerializer(instance=brand, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_brand = update_brand(brand, **serializer.validated_data)
        return Response(BrandSerializer(updated_brand).data, status=status.HTTP_200_OK)