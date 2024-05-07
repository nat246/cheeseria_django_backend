from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import Cheese


@swagger_auto_schema(method='post',
                     request_body=CreateCheeseSerializer, )
@api_view(['POST'])
def create_cheese(request):
    serializer = CreateCheeseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get',
                     responses={200: openapi.Response('Successful response', schema=CheeseSerializer(many=True))})
@api_view(['GET'])
def get_all_cheese(request):
    cheeses = Cheese.objects.all()
    serializer = CheeseSerializer(cheeses, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get',
                     responses={200: openapi.Response('Successful response', schema=CheeseSerializer),
                                404: openapi.Response('Cheese ID not found')})
@api_view(['GET'])
def get_cheese_by_id(request, cheese_id):
    try:
        cheese = Cheese.objects.get(id=cheese_id)
        serializer = CheeseSerializer(cheese)
        return Response(serializer.data)
    except Cheese.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='get',
                     query_serializer=SearchCheeseFilterSerializer(),
                     responses={200: openapi.Response('Successful response', schema=CheeseSerializer)})
@api_view(['GET'])
def get_cheeses_by_search(request):
    search = request.query_params.get('search')
    color = request.query_params.get('color')

    results = Cheese.objects.all()

    if color:
        results = results.filter(color=color)

    if search:
        results = results.filter(Q(name__icontains=search))

    serializer = CheeseSerializer(results, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='patch', request_body=UpdateCheeseSerializer)
@api_view(['PATCH'])
def update_cheese_details(request, cheese_id):
    try:
        cheese = Cheese.objects.get(id=cheese_id)
    except Cheese.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateCheeseSerializer(cheese, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Cheese details updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete')
@api_view(['DELETE'])
def delete_cheese_by_id(request, cheese_id):
    try:
        cheese = Cheese.objects.get(id=cheese_id)
        cheese.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Cheese.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
