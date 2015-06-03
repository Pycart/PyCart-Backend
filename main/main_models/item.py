from django.db import models
from django.db.models import Count
from taggit.managers import TaggableManager
from order import Order
from tag import Shop_Tagged_Item
from datetime import timedelta



class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    tags = TaggableManager(through=Shop_Tagged_Item)
    option = models.ForeignKey("Option")
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return self.name

    @property
    def number_sold(self):
        sold = Order.objects.filter(items=self).count()
        return sold

    @staticmethod
    def get_best_selling():
        orders = Order.objects.all()
        best_selling = Item.objects.filter(order__in=orders).annotate(itemcount=Count('id')).order_by('-itemcount')
        return best_selling

    @staticmethod
    def get_best_selling_recent():
        orders = Order.objects.all()
        date_range = timedelta(days=30)
        best_selling = Item.objects.filter(order__in=orders).annotate(itemcount=Count('id')).order_by('-itemcount')
        best_selling_recent = best_selling.filter(order__date_placed__gte=date_range)
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