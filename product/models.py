from django.db import models
import re


class Cheese(models.Model):
    cheese_colors = (
        ('BLUE', 'BLUE'),
        ('BLUE_GREY', 'BLUE_GREY'),
        ('BROWN', 'BROWN'),
        ('BROWNISH_YELLOW', 'BROWNISH YELLOW'),
        ('GOLDEN_ORANGE', 'GOLDEN ORANGE'),
        ('GOLDEN_YELLOW', 'GOLDEN YELLOW'),
        ('GREEN', 'GREEN'),
        ('IVORY', 'IVORY'),
        ('ORANGE', 'ORANGE'),
        ('PALE_WHITE', 'PALE WHITE'),
        ('PALE_YELLOW', 'PALE_YELLOW'),
        ('PINK_AND_WHITE', 'PINK AND WHITE'),
        ('RED', 'RED'),
        ('STRAW', 'STRAW'),
        ('WHITE', 'WHITE'),
        ('YELLOW', 'YELLOW'),
    )

    id = models.CharField(primary_key=True, unique=True, max_length=30, null=False)
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(null=False)
    image = models.URLField(null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    color = models.CharField(max_length=40, choices=cheese_colors, null=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_id()
        super().save(*args, **kwargs)

    def generate_id(self):
        kebab_name = re.sub(r'\s+', '-', self.name.strip().lower())
        return kebab_name
