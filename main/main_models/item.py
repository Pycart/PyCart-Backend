import datetime

from django.db import models
from django.db.models import Count
from django.utils import timezone
from itertools import chain

from taggit.managers import TaggableManager

from main.main_models.order import Order
from tag import Shop_Tagged_Item


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    tags = TaggableManager(through=Shop_Tagged_Item)
    # options = models.ManyToManyField("Option")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='photos', blank=True, null=True)
    master = models.ForeignKey('self', related_name='variants', null=True, blank=True, db_index=True)
    is_variant = models.BooleanField(default=False)

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
        raise AttributeError("Cannot set attribute")

    def __unicode__(self):
        return self.name

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

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class Option(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'
