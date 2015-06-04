import datetime

from django.utils import timezone
from rest_framework import authentication, permissions
from rest_framework.generics import ListAPIView

from main.main_models.order import Order
from main.serializers import OrderSerializer

class OrdersView(ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class RecentOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        past = timezone.now() - datetime.timedelta(days=30)
        return Order.objects.filter(user=self.request.user, date_placed__gte=past)
