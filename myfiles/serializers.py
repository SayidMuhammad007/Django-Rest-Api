from rest_framework import serializers
from myfiles.models import *

class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = sell
        fields = ('id','name', 'amount', 'price', 'date', 'time', 'status', 'price1', 'user')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ('id','name', 'price1', 'price2', 'date', 'amount')

class SelledSerializer(serializers.ModelSerializer):
    class Meta:
        model = sotilganlar
        fields = ('id','name', 'price', 'customer', 'date', 'time', 'naqd', 'plastik', 'nasiya', 'amount', 'price1')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('id', 'name', 'password', 'position')