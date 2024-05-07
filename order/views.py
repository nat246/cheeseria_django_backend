from django.contrib.auth.decorators import login_required
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import Cheese
from user_api.models import AppUser as User
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer

item_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['cheese_id', 'quantity'],
    properties={
        'cheese_id': openapi.Schema(type=openapi.TYPE_STRING, description='cheese_id'),
        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='quantity'),
    }
)


@swagger_auto_schema(method='post', operation_description="Create a new order",
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         required=['items'],
                         properties={
                             'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=item_schema,
                                                     description='items'),
                         }
                     ))
@api_view(['POST'])
@login_required
def create_order(request):
    data = request.data
    user = User.objects.get(email=request.user.email)
    items = data['items']
    total_cost = 0
    for item in items:
        cheese = Cheese.objects.get(id=item['cheese_id'])
        total_cost += cheese.price * item['quantity']
    data['user'] = user
    data['total_cost'] = total_cost
    serializer = CreateOrderSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        order = serializer.create(data)
        if order:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', operation_description="Get all orders",
                     responses={200: OrderSerializer(many=True)})
@api_view(['GET'])
@login_required
def get_all_orders(request):
    user = User.objects.get(email=request.user.email)
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='delete', operation_description="Delete an order",
                     responses={204: 'No Content'})
@api_view(['DELETE'])
@login_required
def delete_order(request, order_number):
    user = User.objects.get(email=request.user.email)
    order = Order.objects.get(order_number=order_number)
    if order.user == user:
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'You are not authorized to delete this order'}, status=status.HTTP_403_FORBIDDEN)
