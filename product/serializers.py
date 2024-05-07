from rest_framework import serializers
from .models import Cheese


class CheeseSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    color = serializers.ChoiceField(choices=Cheese.cheese_colors)

    class Meta:
        model = Cheese
        fields = '__all__'


class CreateCheeseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    price = serializers.FloatField()

    class Meta:
        model = Cheese
        fields = ['id', 'name', 'description', 'image', 'price', 'color']


class SearchCheeseFilterSerializer(serializers.ModelSerializer):
    search = serializers.CharField(required=False)
    color = serializers.ChoiceField(choices=Cheese.cheese_colors, required=False)

    class Meta:
        model = Cheese
        fields = ['search', 'color']


class UpdateCheeseSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True)
    image = serializers.URLField(required=False, allow_blank=True)
    price = serializers.FloatField(required=False)

    class Meta:
        model = Cheese
        fields = ['description', 'image', 'price']

    def update(self, instance, validated_data):
        # Check if the description field is provided and not empty
        if 'description' in validated_data and (validated_data['description'] != ''):
            instance.description = validated_data['description']

        # Check if the image field is provided and not empty
        if 'image' in validated_data and (validated_data['image'] != ''):
            instance.image = validated_data['image']

        # Update the price field if provided
        if 'price' in validated_data:
            instance.price = validated_data['price']

        instance.save()
        return instance
