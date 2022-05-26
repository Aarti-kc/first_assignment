from rest_framework import serializers
from .models import *

class ProductsSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(max_length=255,default="")
    product_price=serializers.FloatField(default='0')
    description=serializers.CharField(max_length=255,default="")
    product_quantity = serializers.IntegerField(required=False, default=1)


    class Meta:
        model = Products
        fields = ('__all__')