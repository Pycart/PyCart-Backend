import datetime
from decimal import Decimal

from django.db import models
from django.utils import timezone
from main.main_models.user import AbstractShopUser
from main.models import *


class AbstractStatus(models.Model):
    _default = models.BooleanField(default=False)
    abs_status = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        if value:
            current_default = AbstractStatus.objects.get(_default=True)
            current_default._default = False
            current_default.save()
            self._default = True
            self.save()

    class Meta:
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Statuses'

    def __unicode__(self):
        return self.abs_status


class AbstractOrder(models.Model):
    _current_status = models.ForeignKey(AbstractStatus, blank=True, null=True)
    _last_modified = models.DateTimeField(auto_now=True)
    _weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    _total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    user = models.ForeignKey(AbstractShopUser)
    items = models.ManyToManyField('main.Item', through='main.OrderItem')
    placed = models.BooleanField(default=False)
    date_placed = models.DateTimeField(null=True, blank=True)

    # TODO: Add shipping carrier FK
    # shipping = models.ForeignKey()

    def __unicode__(self):
        return unicode(self.id)

    def set_weight(self):
        total = Decimal()
        for order_item in self.abstractorderitem_set.all():
            weight = order_item.item.weight
            quantity = order_item.quantity
            total += weight * quantity
        self._weight = total

    def set_total_price(self):
        total = Decimal()
        for order_item in self.abstractorderitem_set.all():
            price = order_item.item.price
            quantity = order_item.quantity
            total += price * quantity
        self._total_price = total

    def place_order(self):
        self.current_status = AbstractStatus.objects.get(_default=True)
        self.placed = True
        self.date_placed = timezone.now()

    def recently_placed(self):
        # TODO: Make configurable amount of time order stays "recent", probably in settings.py or as a user attribute
        now = timezone.now()
        return now - datetime.timedelta(days=30) <= self.date_placed <= now

    def get_avg_completed_order_total_price(self):
        raise NotImplementedError("Needs to be implemented")

    def get_total_incomplete_orders_count(self):
        raise NotImplementedError("Needs to be implemented")

    @staticmethod
    def average_order_price():
        orders = AbstractOrder.objects.filter(placed=True).count()
        total_cost = sum([order.total_price for order in orders])
        average_order_price = total_cost / orders
        return average_order_price

    @staticmethod
    def incomplete_order_count():
        orders = AbstractOrder.objects.filter(placed=False).count()
        return orders

    @staticmethod
    def average_order_price():
        orders = AbstractOrder.objects.filter(placed=True).count()
        total_cost = sum([order.total_price for order in orders])
        average_order_price = total_cost / orders
        return average_order_price

    @staticmethod
    def incomplete_order_count():
        orders = AbstractOrder.objects.filter(placed=False).count()
        return orders

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
        now = timezone.now()
        self._current_status = status
        self._last_modified = now

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


class AbstractOrderItem(models.Model):
    order = models.ForeignKey(AbstractOrder)
    item = models.ForeignKey('main.Item')
    quantity = models.IntegerField(default=1)
