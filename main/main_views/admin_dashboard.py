from rest_framework import mixins, generics, permissions, authentication
from main.main_models.order import Status
from main.models import Item, Option, ShopUser
from main.serializers import ItemSerializer, OptionSerializer, StatusSerializer, ShopUserSerializer


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

# TODO: When we query, we will want to filter out the Admins from this list.
class AdminShopUserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = ShopUser.objects.all()
    serializer_class = ShopUserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)