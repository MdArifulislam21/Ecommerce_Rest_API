from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from django.db import transaction

from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "product",
            "quantity",
            "price",
            "cost",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("order",)

    def validate(self, validated_data):
        order_quantity = validated_data["quantity"]
        product_quantity = validated_data["product"].quantity

        order_id = self.context["view"].kwargs.get("order_id")
        product = validated_data["product"]
        current_item = OrderItem.objects.filter(order__id=order_id, product=product)

        if order_quantity > product_quantity:
            error = {"quantity": _("Ordered quantity is more than the stock.")}
            raise serializers.ValidationError(error)

        if not self.instance and current_item.count() > 0:
            error = {"product": _("Product already exists in your order.")}
            raise serializers.ValidationError(error)

        if self.context["request"].user == product.seller:
            error = _("Adding your own product to your order is not allowed")
            raise PermissionDenied(error)

        return validated_data

    def get_price(self, obj):
        return obj.product.price

    def get_cost(self, obj):
        return obj.cost


class OrderReadSerializer(serializers.ModelSerializer):

    buyer = serializers.CharField(source="buyer.get_full_name", read_only=True)
    order_items = OrderItemSerializer(read_only=True, many=True)
    total_cost = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "buyer",
            "shipping_address",
            "billing_address",
            # "payment",
            "order_items",
            "total_cost",
            "status",
            "created_at",
            "updated_at",
        )

    def get_total_cost(self, obj):
        return obj.total_cost


class OrderWriteSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating orders and order items

    Shipping address, billing address and payment are not included here
    They will be created/updated on checkout
    """

    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "buyer",
            "status",
            "order_items",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status",)

    def create(self, validated_data):
        orders_data = validated_data.pop("order_items")
        
        try:
            with transaction.atomic():
                order = Order.objects.create(**validated_data)

                for order_data in orders_data:
                    product = order_data.get('product')
                    quantity = order_data.get('quantity')
                    if product.quantity > quantity:
                        product.quantity -= quantity
                        product.save()
                    else:
                        raise serializers.ValidationError( _("Product doesn't have enough quantity"))
                    OrderItem.objects.create(order=order, **order_data)
            transaction.commit()
        
        except Exception as e:
            # If an exception occurs, roll back the changes
            
            transaction.rollback()
            
        return order

    def update(self, instance, validated_data):
        order_items = validated_data.pop("order_items", None)
        instance_order_items = list((instance.order_items).all())

        if order_items:
            for order_item in order_items:
                item = instance_order_items.pop(0)
                product = order_item.get("product", item.product)
                quantity = order_item.get("quantity", item.quantity)
                
                if order_item.get("quantity"):
                    
                    """ Check if product has enought quantity in stock """
                    
                    if product.quantity < quantity - item.quantity:
                        raise serializers.ValidationError( _("Product doesn't have enough quantity"))
                    
                    product.quantity -= quantity - item.quantity
                    
                item.product = product 
                item.quantity = quantity
                item.save()

        return instance
