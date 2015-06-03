from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from order import Order

@receiver(m2m_changed, sender=Order.items.through)
def update_order_when_items_changed(sender, instance, **kwargs):
    instance.set_weight()
    instance.set_total_price()
    instance.save()

