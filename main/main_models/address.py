from django.db import models


class Address(models.Model):
    options = {
        "Billing": "Billing",
        "Shipping": "Shipping"
    }
    type = models.CharField(max_length=20, choices=(options,))
    name = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    apt = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=10)
    zip = models.CharField(max_length=10)
    user = models.ForeignKey("ShopUser")

    def __unicode__(self):
        return self.name
