from django.urls import path
from .views import StoreInventoryListAPIView,StoreListAPIView

urlpatterns = [
    path('<int:store_id>/inventory/', StoreInventoryListAPIView.as_view(), name='store-inventory-list'),
    path('', StoreListAPIView.as_view(), name='store-list'),
]
