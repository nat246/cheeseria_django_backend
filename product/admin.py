from django.contrib import admin
from .models import Cheese


# Register your models here.
class CheeseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'color')


admin.site.register(Cheese, CheeseAdmin)
