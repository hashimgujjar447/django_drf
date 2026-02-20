from rest_framework import serializers
from .models import Product,Order,OrderItem
from django.contrib.auth import get_user_model

user=get_user_model()




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        exclude=('password',)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=(
            'name',
            'description',
            'price',
            'stock'
        )

    def validate_price(self,value):
        if value<=0:
            raise serializers.ValidationError(
                "Value must be greater than 0"
            )
        return value
            

class OrderItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name', read_only=True)
    product_price=serializers.CharField(source='product.price', read_only=True)

   
        
    class Meta:
        model=OrderItem
        fields=(
            'product',
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal'
        )

class OrderSerializer(serializers.ModelSerializer):
    order_id=serializers.UUIDField(read_only=True)
    items=OrderItemSerializer(many=True, read_only=True)
    total_price=serializers.SerializerMethodField()
 
    def get_total_price(self,obj):
        order_items=obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model=Order
        fields=(
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price'
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model=OrderItem
            fields=('product','quantity')
    items=OrderItemCreateSerializer(many=True)   

    def create(self, validated_data):
        order_items=validated_data.pop('items')
        order=Order.objects.create(**validated_data)
        for item in order_items:
            OrderItem.objects.create(order=order,**item)
        return order    
    def update(self, instance, validated_data):
            order_items = validated_data.pop('items', None)

            # Update simple fields safely
            instance.status = validated_data.get("status", instance.status)
            instance.user = validated_data.get("user", instance.user)
            instance.save()

            # Update items if provided
            if order_items is not None:
                instance.items.all().delete()

                for item in order_items:
                    OrderItem.objects.create(order=instance, **item)

            return instance
            

    class Meta:
        model=Order
        fields=(
           
            'user',
            'status',
            'items',
        )


class ProductInfoSerializer(serializers.Serializer):
    products=ProductSerializer(many=True)
    count=serializers.IntegerField()
    max_price=serializers.FloatField()
    
