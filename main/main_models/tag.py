from django.db import models
from taggit.models import TagBase, GenericTaggedItemBase
from mptt.models import MPTTModel, TreeForeignKey

class Shop_Tagged_Item(GenericTaggedItemBase):
    tag = models.ForeignKey("Shop_Item_Tag")
    date_modified = models.DateTimeField(auto_now = True, null=True)
    date_created = models.DateTimeField(auto_now_add = True, null=True)
    start_date = models.DateTimeField(blank=True, null=True, db_index=True)
    end_date = models.DateTimeField(blank=True, null=True, db_index=True)

    def __unicode__(self):
        return self.tag

    class Meta:
        verbose_name = 'Tagged Item'
        verbose_name_plural = 'Tagged Items'


class Shop_Item_Tag(MPTTModel, TagBase):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    is_browseable = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now = True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Item Tag'
        verbose_name_plural = 'Item Tags'