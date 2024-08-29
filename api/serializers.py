from rest_framework import serializers
from .models import Products, Warehouse, Partys, Buyers

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
    def create(self, validated_data):
        return Products.objects.create(**validated_data)

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class PartysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partys
        fields = '__all__'

class BuyersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyers
        fields = '__all__'
