from rest_framework import generics
from main.serializers import UserDetailSerializer
from main.main_models.user import ShopUser


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopUser.objects.all()
    serializer_class = UserDetailSerializer