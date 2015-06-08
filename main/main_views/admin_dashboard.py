from rest_framework import generics, permissions, authentication
from main.main_models.order import Status
from main.models import Item, Option
from main.serializers import ItemSerializer, OptionSerializer, StatusSerializer


class AdminListCreateItem(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class AdminItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class AdminListCreateOption(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class AdminOptionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class AdminListCreateStatus(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class AdminStatusDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
