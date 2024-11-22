from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product, User
from .serializers import ProductSerializer
from rest_framework.views import APIView
import random
from .producer import publish

# ViewSet for Product model
class ProductViewSet(viewsets.ViewSet):
    # List all products
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # Create a new product
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product created', serializer.data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # Retrieve a specific product
    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

    # Update an existing product
    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                publish('product updated', serializer.data)
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Product.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

    # Delete a product
    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            publish('Product deleted', pk)
            return Response(status=204)
        except Product.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)


# User API View
class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()

        # Check if there are any users
        if users.exists():
            user = random.choice(users)
            return Response({'id': user.id})
        else:
            return Response({'detail': 'No users available'}, status=404)
