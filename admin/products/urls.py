from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, UserAPIView

# Create a router and register the ProductViewSet with it
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('user', UserAPIView.as_view())
]
