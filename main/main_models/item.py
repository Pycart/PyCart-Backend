# import datetime
# from itertools import chain
# from django.db import models
# from django.db.models import Count
# from django.utils import timezone
# from taggit.managers import TaggableManager
#
# #from main.models import Order
#
#
# class AbstractItem(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     weight = models.DecimalField(max_digits=6, decimal_places=2)
#     tags = TaggableManager(through='main.ShopTaggedItem')
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     image = models.ImageField(upload_to='photos', blank=True, null=True)
#     master = models.ForeignKey('main.Item', related_name='variants', null=True, blank=True, db_index=True)
#
#     class Meta:
#         db_table = "main_item"
#         app_label = "main"
#         #abstract = True
#
#     def get_all_variants(self, include_self=False):
#         qs = []
#         if include_self:
#             qs.append(self)
#         for item in AbstractItem.objects.filter(master=self):
#             qs.extend(item.get_all_variants(include_self=True))
#         return chain([q for q in qs])
#
#     def get_top_level_item(self):
#         upper = self
#         if self.is_variant:
#             upper = self.master.get_top_level_item()
#         return upper
#
#     @property
#     def top_level_item(self):
#         return self.get_top_level_item().id
#
#     @top_level_item.setter
#     def top_level_item(self, value):
#         raise AttributeError("Cannot set top level item directly")
#
#     @property
#     def is_variant(self):
#         if self.master is None:
#             return False
#         return True
#
#     @property
#     def number_sold(self):
#         sold = Order.objects.filter(items=self, placed=True).count()
#         return sold
#
#     @staticmethod
#     def get_best_selling():
#         orders = Order.objects.all()
#         best_selling = AbstractItem.objects.filter(order__in=orders, order__placed=True).annotate(
#             itemcount=Count('id')).order_by('-itemcount')
#         return best_selling
#
#     @staticmethod
#     def get_best_selling_recently(days=30):
#         date_range = timezone.now() - datetime.timedelta(days=days)
#         best_selling_recent = AbstractItem.get_best_selling().filter(order__date_placed__gte=date_range)
#         return best_selling_recent
#
#     def __unicode__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Item'
#         verbose_name_plural = 'Items'
#
#
# class AbstractOption(models.Model):
#     name = models.CharField(max_length=255)
#
#     def __unicode__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Option'
#         verbose_name_plural = 'Options'
#
