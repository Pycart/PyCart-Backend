from rest_framework import generics
from main.models import Order
from main.serializers import OrderDetailSerializer


# TODO: Refactor to Retrieve API View as we don't want users to be able to change Order details after it has been placed
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer



