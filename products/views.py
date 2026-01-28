from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, F
from .models import Product
from stores.models import Inventory
from .serializers import ProductSearchSerializer

class ProductSearchAPIView(APIView):
    def get(self, request):
        queryset = Product.objects.all()

        
        q = request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )

        
        category_id = request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        min_price = request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        store_id = request.GET.get('store_id')
        in_stock = request.GET.get('in_stock') == 'true'

        if store_id:
            queryset = queryset.annotate(quantity_in_store=F('inventory__quantity'))\
                               .filter(inventory__store_id=store_id)
            if in_stock:
                queryset = queryset.filter(inventory__quantity__gt=0)

        # Sorting happens here
        sort = request.GET.get('sort')
        if sort == 'price':
            queryset = queryset.order_by('price')
        elif sort == '-price':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('-id')

        # Pagination happens here
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = ProductSearchSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

