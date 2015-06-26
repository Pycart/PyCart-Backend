from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver((post_save, post_delete), sender='main.OrderItem')
def update_order_when_items_changed(sender, instance, **kwargs):
    order = instance.order
    order.set_weight()
    order.set_total_price()
    order.save()
