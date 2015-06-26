from django.db import models


class AbstractStockRecord(models.Model):
    item = models.ForeignKey("main.Item")
    qty = models.IntegerField(default=0)
    vendor = models.CharField(max_length=255)

