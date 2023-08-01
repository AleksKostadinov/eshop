# models.py
from django.db import models
from accounts.models import Account
from shop_app.models import Product, Variation

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    variations = models.ManyToManyField(Variation, blank=True)

    def sub_total(self):
        return self.product.discounted_price * self.quantity

    def __str__(self):
        return f"{self.cart}"
