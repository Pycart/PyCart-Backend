import datetime

from django.utils import timezone
from rest_framework import authentication, permissions, status
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response

from main.main_models.order import Order
from main.serializers import OrderSerializer, AddToOrderSerializer


class OrdersView(ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class RecentOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        past = timezone.now() - datetime.timedelta(days=30)
        return Order.objects.filter(user=self.request.user, placed=True, date_placed__gte=past)


class GetCart(RetrieveAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        order = Order.objects.get(user=self.request.user, placed=False)
        return order


class AddItemToOrderView(UpdateAPIView):
    serializer_class = AddToOrderSerializer
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        # item_indexes = self.request.data.pop('items')
        # items = []
        # for index in item_indexes:
        #     if type(index) == int:
        #         item = Item.objects.get(pk=index)
        #         serialized_item = ItemSerializer(item).data
        #         items.append(serialized_item)
        #     else:
        #         item = Item.objects.get(pk=index['id'])
        #         serialized_item = ItemSerializer(item).data
        #         items.append(serialized_item)
        #
        # self.request.data['items'] = items

        serializer = AddToOrderSerializer(data=self.request.data)
        if serializer.is_valid():
            order = serializer.update(self.get_object(), serializer.validated_data)
            return Response('Item Added', status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        order = Order.objects.filter(user=self.request.user, placed=False).first()
        if not order:
            order = Order(user=self.request.user, placed=False)
            order.save()
        return order
