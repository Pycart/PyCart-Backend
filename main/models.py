#python
import datetime
import signals
from itertools import chain

#django
from django.db.models import Count
from django.utils import timezone
from django.db import models

#models
from main.main_models.user import *
from main.main_models.address import *
from main.main_models import order
from main.main_models.save_card import *
from main.main_models.stock_record import *
from main.main_models.tag import *

from taggit.managers import TaggableManager


class ShopUserManager(AbstractCustomUserManager):
    pass


class ShopUser(AbstractShopUser):
    object = ShopUserManager()
    pass


class Address(AbstractAddress):
    pass


class Order(order.AbstractOrder):
    pass


class OrderItem(order.AbstractOrderItem):
    pass


class Status(order.AbstractStatus):
    pass


class SaveCard(AbstractSaveCard):
    pass

class StockRecord(AbstractStockRecord):
    pass


class ShopItemTag(AbstractShopItemTag):
    pass


class ShopTaggedItem(AbstractShopTaggedItem):
    pass


class SavedCard(AbstractSaveCard):
    pass


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    tags = TaggableManager(through='main.ShopTaggedItem')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='photos', blank=True, null=True)
    master = models.ForeignKey('main.Item', related_name='variants', null=True, blank=True, db_index=True)

    def get_all_variants(self, include_self=False):
        qs = []
        if include_self:
            qs.append(self)
        for item in Item.objects.filter(master=self):
            qs.extend(item.get_all_variants(include_self=True))
        return chain([q for q in qs])

    def get_top_level_item(self):
        upper = self
        if self.is_variant:
            upper = self.master.get_top_level_item()
        return upper

    @property
    def top_level_item(self):
        return self.get_top_level_item().id

    @top_level_item.setter
    def top_level_item(self, value):
        raise AttributeError("Cannot set top level item directly")

    @property
    def is_variant(self):
        if self.master is None:
            return False
        return True

    @property
    def number_sold(self):
        sold = Order.objects.filter(items=self, placed=True).count()
        return sold

    @staticmethod
    def get_best_selling():
        orders = Order.objects.all()
        best_selling = Item.objects.filter(order__in=orders, order__placed=True).annotate(
            itemcount=Count('id')).order_by('-itemcount')
        return best_selling

    @staticmethod
    def get_best_selling_recently(days=30):
        date_range = timezone.now() - datetime.timedelta(days=days)
        best_selling_recent = Item.get_best_selling().filter(order__date_placed__gte=date_range)
        return best_selling_recent

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'



# To prevent code cleanup from removing signals from imports
if signals:
    pass
