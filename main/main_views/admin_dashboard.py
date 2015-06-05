from rest_framework import generics, permissions
from main.models import Item, Option
from main.serializers import AdminCreateItemSerializer, AdminItemListSerializer, AdminItemDetailSerializer, \
    AdminCreateOptionSerializer, AdminOptionListSerializer, AdminOptionDetailSerializer


class AdminCreateItem(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Item.objects.all()
    serializer_class = AdminCreateItemSerializer


class AdminItemList(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Item.objects.all()
    serializer_class = AdminItemListSerializer


class AdminItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Item.objects.all()
    serializer_class = AdminItemDetailSerializer


class AdminCreateOption(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Option.objects.all()
    serializer_class = AdminCreateOptionSerializer


class AdminOptionList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Option.objects.all()
    serializer_class = AdminOptionListSerializer


class AdminOptionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Option.objects.all()
    serializer_class = AdminOptionDetailSerializer
