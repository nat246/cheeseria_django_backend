from rest_framework import serializers
from .models import Order
from user_api.models import AppUser as User


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = serializers.JSONField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = ['user', 'items', 'total_cost', 'status', 'order_date']


class UpdateOrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField()

    class Meta:
        model = Order
        fields = ['status']

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance
