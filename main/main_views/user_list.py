from rest_framework import mixins, generics
from main.main_models.user import ShopUser
from main.serializers import ShopUserSerializer



class ShopUserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ShopUser.objects.all()
    serializer_class = ShopUserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)