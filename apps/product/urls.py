from django.urls import include, path
from django.conf import settings
from rest_framework import routers

from apps.product.views import CreateProduct, UpdateProduct, getProduct, DeleteProduct

router = routers.SimpleRouter()

router.register(r'create', CreateProduct, basename='create')
router.register(r'update', UpdateProduct, basename='update')
router.register(r'get', getProduct, basename='get')
router.register(r'delete', DeleteProduct, basename='delete')

urlpatterns = [
    path('', include(router.urls)),
]