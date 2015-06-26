from rest_framework import generics
from main.serializers import TagSerializer
from main.models import ShopItemTag


class TagList(generics.ListAPIView):
    queryset = ShopItemTag.objects.all()
    serializer_class = TagSerializer


class HeaderTagList(generics.ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = ShopItemTag.objects.filter(level=0)
        return queryset


class SubheaderTagList(generics.ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = ShopItemTag.objects.filter(level=1)
        return queryset