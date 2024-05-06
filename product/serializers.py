from rest_framework import serializers
from .models import Cheese


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheese
        fields = '__all__'
