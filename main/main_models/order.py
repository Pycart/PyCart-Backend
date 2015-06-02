from django.db import models
from django.utils import timezone
from user import ShopUser
from item import Item
import uuid

class Status(models.Model):
    status = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Statuses'

    def __unicode__(self):
        return self.status

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4().int, editable=False, unique=True)

    _current_status = models.ForeignKey(Status)
    _current_status_last_modified = models.DateTimeField(auto_now_add=True)
    _weight = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(ShopUser)
    items = models.ManyToManyField(Item)
    date_placed = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # TODO: Add shipping carrier FK
    # shipping = models.ForeignKey()

    def __unicode__(self):
        return unicode(self.id)

    def set_weight(self):
        total = 0.0
        for item in self.items.all():
            total += item.weight
        self.weight = total

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
        self._current_status_date_modified = now

    @property
    def current_status_last_modified(self):
        return self._current_status_last_modified

    @current_status_last_modified.setter
    def current_status_last_modified(self, value):
        raise AttributeError("You cannot set the date last modified directly. "
                             "Updating the status will do this for you.")
