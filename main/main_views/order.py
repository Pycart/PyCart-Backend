import datetime

from django.conf import settings
from django.utils import timezone
from rest_framework import authentication, permissions, status
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response


from main.models import Order
from main.serializers import OrderSerializer, ItemOrderUpdateSerializer


class OrdersView(ListAPIView):
    """
    Returns a list of all this users orders.
    """
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    if settings.DEBUG:
        authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Should return all orders that the user has placed successfully.
        return Order.objects.filter(user=self.request.user, placed=True)


class RecentOrdersView(ListAPIView):
    """
    Returns a list of all this users recent orders. By default its 30 days.
    """
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
        order = Order.objects.filter(user=self.request.user, placed=False).first()
        if not order:
            order = Order(user=self.request.user, placed=False)
            order.save()
        return order


class UpdateCart(UpdateAPIView):
    """
    This view takes in two lists, 'items' and 'quantity'. The items list is a set of item ID's that the user would
    like to add to an order. The quantities list is the amount of each item.

    The use of the increment flag would determine if you are adding that many to existing item on an order.
    If the increment flag is set to false, it will set that order quantity to that exact amount.
    If the increment flag is set to True, negative quantities are no longer ignored and will
    subtract from the total items. If at that point the total for that item is less than 0 it will be removed.

    By default increment is True. To remove items you must explicitly set increment to False and set an items
    quantity to 0.

    For example:

    An order is in progress and it has these items already on it:

    Item 1, quantity 8.
    Item 2, quantity 2.
    Item 7, quantity 5.
    Item 8, quantity 5.

    A request to update the cart with an Increment True was made:
    {
        Items: [1, 6, 7, 8],
        Quantity: [3, 5, -3, 0],
        Increment: True
    }

    Afterwards, the items on the order look like this:

    Item 1, quantity 11.
    Item 2, quantity 2.
    Item 6 was created with a quantity of 5.
    Item 7, quantity 2.
    Item 8, quantity 5.


    Example 2:

    An order is in progress and it has these items already on it:

    Item 1, quantity 8.
    Item 2, quantity 2.
    Item 7, quantity 5.
    Item 8, quantity 5.

    A request to update the cart with a increment of False is made.

    {
        Items:    [1, 6, 7, 8],
        Quantity: [3, 1, 0, -2],
        Increment: False
    }

    Afterwards, the items on the order look like this:

    Item 1, quantity 3.
    Item 2, quantity 2.
    Item 6 was created with a quantity of 1.
    Item 7 was removed.
    Item 8, quantity 5.
    """
    serializer_class = ItemOrderUpdateSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    if settings.DEBUG:
        authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        print request.DATA
        serializer = ItemOrderUpdateSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.update(self.get_object(), serializer.validated_data)
            return Response('Items Updated', status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        order = Order.objects.filter(user=self.request.user, placed=False).first()
        if not order:
            order = Order(user=self.request.user, placed=False)
            order.save()
        return order
