from rest_framework import generics
from main.main_models.item import Option
from main.models import Item
from main.serializers import ItemDetailSerializer, OptionSerializer


# TODO: Change to Retrieve API View
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


class OptionList(generics.ListAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
