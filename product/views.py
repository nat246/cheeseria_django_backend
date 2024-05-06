from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import ProductSerializer
from .models import Cheese


# Create your views here.
class ProductView(viewsets.ModelViewSet):
    queryset = Cheese.objects.all()
    serializer_class = ProductSerializer
