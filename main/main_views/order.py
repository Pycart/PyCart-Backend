import datetime

from django.conf import settings
from django.utils import timezone
from rest_framework import authentication, permissions, status
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response


from main.main_models.order import Order
from main.serializers import OrderSerializer, AddToOrderSerializer


class OrdersView(ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    if settings.DEBUG:
        authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Should return all orders that the user has placed successfully.
        return Order.objects.filter(user=self.request.user, placed=True)


class RecentOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    if settings.DEBUG:
        authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        past = timezone.now() - datetime.timedelta(days=30)
        # Should return all orders that the user has placed successfully within the last 30 days.
        return Order.objects.filter(user=self.request.user, placed=True, date_placed__gte=past)


class GetCart(RetrieveAPIView):
    """
    Returns current cart that the user has. A 'cart' is defined as an order that has not been placed.
    Once the order has been processed it will then be moved to a 'placed' status and moved to the orders list.
    """
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    if settings.DEBUG:
        authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        order = Order.objects.get(user=self.request.user, placed=False)
        return order


class AddItemToOrderView(UpdateAPIView):
    """
    This view takes in two lists, 'items' and 'quantity'. The items list is a set of item ID's that the user would
    like to add to an order. Then in the quantities list the amount of each item that user would like. A quantity of 0
    would remove the item from the cart, if it exists already. Other wise, it would be ignored.

    For example:
    {
        Items: [1, 3, 6, 7]
        Quantity: [3, 0, 1, 1]
    }

    The input above would add the Item with index of 1 with a quantity of 3 to the cart,
     it would delete the Item with an ID of 3 from the cart, add the Item with the ID of 6 to the cart with a
     quantity of 1 and finally would add the Item with the ID of 7 to the cart with a quantity of 1 as well.
    """
    serializer_class = AddToOrderSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    if settings.DEBUG:
        authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        serializer = AddToOrderSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.update(self.get_object(), serializer.validated_data)
            return Response('Item Added', status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        order = Order.objects.filter(user=self.request.user, placed=False).first()
        if not order:
            order = Order(user=self.request.user, placed=False)
            order.save()
        return order
