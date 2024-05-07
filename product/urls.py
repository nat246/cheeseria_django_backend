from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', create_cheese, name='create-cheese'),
    path('cheese/', get_cheeses_by_search, name='get-cheese-by-search'),
    path('cheese/all', get_all_cheese, name='get-all-cheese'),
    path('cheese/<str:cheese_id>', get_cheese_by_id, name='get-cheese-by-id'),
    path('cheese/<str:cheese_id>/update', update_cheese_details, name='update-cheese-by-id'),
    path('cheese/<str:cheese_id>/delete', delete_cheese_by_id, name='delete-fun'),
]

urlpatterns += router.urls
