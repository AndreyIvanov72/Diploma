from rest_framework import serializers
from .models import Shop, Category, Product, ProductInfo, Order, OrderItem, Contact

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.SerializerMethodField()
    class Meta:
        model = ProductInfo
        fields = ['id', 'name', 'product', 'shop', 'shop_name', 'price', 'price_rrc', 'quantity']
    def get_shop_name(self, obj):
        return obj.shop.name

class ProductInfoSerializer(serializers.ModelSerializer):
    shop_name = serializers.SerializerMethodField()
    class Meta:
        model = ProductInfo
        fields = ['id', 'name', 'product', 'shop', 'shop_name', 'price', 'price_rrc', 'quantity']
    def get_shop_name(self, obj):
        return obj.shop.name

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'dt', 'product', 'status']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'address', 'phone', 'email']
