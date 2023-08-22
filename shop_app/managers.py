from django.db import models
from django.db.models import Avg


class VariationManager(models.Manager):
    def colors(self):
        return super().filter(variation_category='color', is_active=True)
    def sizes(self):
        return super().filter(variation_category='size', is_active=True)


class ProductManager(models.Manager):
    def top_by_rating(self):
        return self.annotate(avg_rating=Avg('reviewrating__rating')).order_by('-avg_rating')[:6]
