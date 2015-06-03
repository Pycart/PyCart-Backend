from rest_framework import generics
from main.models import Item
from main.serializers import ItemSerializer


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Item.objects.filter()
    queryset = Item.objects.all()
    serializer_class = ItemSerializer