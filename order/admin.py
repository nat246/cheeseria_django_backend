from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'order_date', 'total_cost', 'status']
    list_filter = ['order_date', 'status']
    search_fields = ['order_number', 'user__username']


admin.site.register(Order)

