from rest_framework import serializers
from django.db import transaction
from stores.models import Inventory
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity_requested']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "store", "status", "created_at", "items"]
        read_only_fields = ["status", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            # Check inventory for each item
            insufficient_stock = []
            for item in items_data:
                try:
                    inventory = Inventory.objects.get(
                        store=validated_data['store'],
                        product=item["product"]
                    )
                    if inventory.quantity < item["quantity_requested"]:
                        insufficient_stock.append(item["product"].title)
                except Inventory.DoesNotExist:
                    insufficient_stock.append(item["product"].title)

            # Reject if any product insufficient
            if insufficient_stock:
                order.status = "REJECTED"
                order.save()
                return order

            # Deduct stock and create OrderItems
            for item in items_data:
                inventory = Inventory.objects.get(
                    store=validated_data['store'],
                    product=item["product"]
                )
                inventory.quantity -= item["quantity_requested"]
                inventory.save()

                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity_requested=item["quantity_requested"]
                )

            
            order.status = "CONFIRMED"
            order.save()

        return order



class OrderListSerializer(serializers.ModelSerializer):
    total_items = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "total_items"]


