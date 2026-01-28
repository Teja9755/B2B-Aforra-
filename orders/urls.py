from django.urls import path
from .views import OrderCreateAPIView,StoreOrdersListAPIView

urlpatterns = [
    path('orders/', OrderCreateAPIView.as_view(), name='order-create'),
     path('stores/<int:store_id>/orders/', StoreOrdersListAPIView.as_view(), name='store-orders-list'),
]
