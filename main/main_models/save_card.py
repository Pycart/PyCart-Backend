from django.db import models


class SaveCard(models.Model):
    name = models.CharField(max_length=30)
    #Stripe reference
    ref = models.CharField(max_length=255)
    user = models.ForeignKey("main.ShopUser")

    def __unicode__(self):
        return self.name


