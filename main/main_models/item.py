from django.db import models
from taggit.managers import TaggableManager
from tag import Shop_Tagged_Item


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    tags = TaggableManager(through=Shop_Tagged_Item)
    option = models.ForeignKey("Option")
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return self.name

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