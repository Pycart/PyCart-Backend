from rest_framework import generics
from main.models import Order
from main.serializers import OrderDetailSerializer


# TODO: Change to Retrieve API View
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer



