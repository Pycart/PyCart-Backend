from django.db import models
from user import ShopUser
from item import Item
import uuid

class Status(models.Model):
    status = models.CharField()
    description = models.CharField()

    def __str__(self):
        return self.status

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ShopUser)
    items = models.ManyToManyField(Item)
    current_status = models.ForeignKey(Status)
    date_placed = models.DateTimeField(auto_now_add=True)
    weight = models.DecimalField(max_digits=10, 2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # TODO: Add shipping carrier FK
    # shipping_carrier = models.ForeignKey()

    # TODO: Expected ship date
    # Would depend heavily on shipping method. Not sure if we want to implement it here or in the shipping models.
    # expected_shipping_date = models.DateField

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def get_status(self):
        return self.current_status.status

    def set_weight(self):
        total = 0.0
        for item in self.items.all():
            total += item.weight
        self.weight = total
        return True

