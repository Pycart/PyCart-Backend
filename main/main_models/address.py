from django.db import models
from user import ShopUser


class Address(models.Model):
    options = {
        "Billing": "Billing",
        "Shipping": "Shipping"
    }
    type = models.CharField(max_length=20, choices=options)
    name = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    apt = models.CharField(max_length=30)blank=True)
    city = models.CharField(max_length=30)
    state =models.CharField(max_length=10)
    zip = models.CharField(max_length=10)
    user = models.ForeignKey("ShopUser")

    def __unicode__(self):
        return self.name



# have an address typefield, then give it a foreign key going back to user.
# add all of the standard address attributes
# start filling in the user dashboard (will have all of the user information, except the user model)

#  User CC address
# User Shipping
