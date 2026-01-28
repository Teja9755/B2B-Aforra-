from rest_framework.views import APIView
from rest_framework.response import Response
from stores.models import Inventory,Store
from .serializers import InventorySerializer,StoreSerializer

class StoreInventoryListAPIView(APIView):
    def get(self, request, store_id):
        
        inventory_qs = Inventory.objects.filter(store_id=store_id)\
            .select_related('product', 'product__category')\
            .order_by('product__title')  

        serializer = InventorySerializer(inventory_qs, many=True)
        return Response(serializer.data)

class StoreListAPIView(APIView):
    def get(self, request):
        stores = Store.objects.all().order_by('id') 
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)