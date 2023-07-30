from django.db import models
from accounts.models import Account
from shop_app.models import Product


class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def sub_total(self):
        return self.product.discounted_price * self.quantity

    def __str__(self):
        return self.product
