from decimal import Decimal
from datetime import date, datetime
from django.db import models
from django.utils import timezone
from user import ShopUser
from item import Item

class Status(models.Model):
    status = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Statuses'

    def __unicode__(self):
        return self.status

class Order(models.Model):
    _current_status = models.ForeignKey(Status)
    _last_modified = models.DateTimeField(auto_now=True)
    _weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    _total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    user = models.ForeignKey(ShopUser)
    items = models.ManyToManyField(Item)
    date_placed = models.DateTimeField(auto_now_add=True)

    # TODO: Add shipping carrier FK
    # shipping = models.ForeignKey()

    def __unicode__(self):
        return unicode(self.id)

    def set_weight(self):
        total = Decimal()
        for item in self.items.all():
            total += item.weight
        self._weight = total

    def set_total_price(self):
        total = Decimal()
        for item in self.items.all():
            total += item.price
        self._total_price = total

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        raise AttributeError("Cannot set weight directly! "
                             "calc_weight() will set the weight based on items in the order.")

    @property
    def current_status(self):
        return self._current_status

    @current_status.setter
    def current_status(self, status):
        now = datetime.now()
        self._current_status = status
        self._current_status_date_modified = now

    @property
    def last_modified(self):
        return self._last_modified

    @last_modified.setter
    def last_modified(self, value):
        raise AttributeError("You cannot set the date last modified directly.")

    @property
    def total_price(self):
        return self._total_price

    @total_price.setter
    def total_price(self, value):
        raise AttributeError("You cannot set the total price directly. It is calculated via all the items prices.")
