from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('all/', get_all_orders, name='get_all_orders'),
    path('delete/<int:order_number>/', delete_order, name='delete_order'),
]

