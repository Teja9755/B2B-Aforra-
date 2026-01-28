from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer,OrderListSerializer
from django.db.models import Count
from .models import Order
from .tasks import send_order_confirmation


class OrderCreateAPIView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            customer_email = request.data.get('email')  
            send_order_confirmation.delay(order.id, customer_email)
            return Response(OrderSerializer(order).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoreOrdersListAPIView(APIView):
    def get(self, request, store_id):
       
        orders = Order.objects.filter(store_id=store_id)\
            .annotate(total_items=Count('items'))\
            .order_by('-created_at')  

        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)
