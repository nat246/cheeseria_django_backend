from django.db import models
from user_api.models import AppUser as User
from product.models import Cheese


class Order(models.Model):
    statuses = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )

    order_number = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    items = models.JSONField(blank=False)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=statuses, default='pending')

    def __str__(self):
        return str(self.order_number)
