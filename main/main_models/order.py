import datetime
from decimal import Decimal

from django.db import models
from django.utils import timezone


class Status(models.Model):
    status = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Statuses'

    def __unicode__(self):
        return self.status


class OrderItem(models.Model):
    order = models.ForeignKey('main.Order')
    item = models.ForeignKey('main.Item')
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    _current_status = models.ForeignKey("main.Status", blank=True, null=True)
    _last_modified = models.DateTimeField(auto_now=True)
    _weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    _total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    user = models.ForeignKey("main.ShopUser")
    items = models.ManyToManyField("main.Item", through='main.OrderItem')
    placed = models.BooleanField(default=False)
    date_placed = models.DateTimeField(null=True, blank=True)

    # TODO: Add shipping carrier FK
    # shipping = models.ForeignKey()

    def __unicode__(self):
        return unicode(self.id)

    def set_weight(self):
        total = Decimal()
        for order_item in self.orderitem_set.all():
            weight = order_item.item.weight
            quantity = order_item.quantity
            total += weight * quantity
        self._weight = total

    def set_total_price(self):
        total = Decimal()
        for order_item in self.orderitem_set.all():
            price = order_item.item.price
            quantity = order_item.quantity
            total += price * quantity
        self._total_price = total

    def place_order(self):
        raise NotImplementedError("Needs to be implemented")

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
        orders = Order.objects.filter(placed=True).count()
        total_cost = sum([order.total_price for order in orders])
        average_order_price = total_cost / orders
        return average_order_price

    @staticmethod
    def incomplete_order_count():
        orders = Order.objects.filter(placed=False).count()
        return orders

    @staticmethod
    def average_order_price():
        orders = Order.objects.filter(placed=True).count()
        total_cost = sum([order.total_price for order in orders])
        average_order_price = total_cost / orders
        return average_order_price

    @staticmethod
    def incomplete_order_count():
        orders = Order.objects.filter(placed=False).count()
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
