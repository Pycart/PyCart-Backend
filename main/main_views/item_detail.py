from rest_framework import generics
from main.models import Item
from main.serializers import ItemDetailSerializer


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer