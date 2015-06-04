from rest_framework import generics
from main.serializers import TagSerializer
from main.main_models.tag import Shop_Item_Tag


class TagList(generics.ListAPIView):
    queryset = Shop_Item_Tag.objects.all()
    serializer_class = TagSerializer


class HeaderTagList(generics.ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Shop_Item_Tag.objects.filter(level=0)
        return queryset


class SubheaderTagList(generics.ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Shop_Item_Tag.objects.filter(level=1)
        return queryset