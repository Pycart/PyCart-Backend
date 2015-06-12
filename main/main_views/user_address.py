from rest_framework import generics
from main.models import Address
from main.serializers import AddressSerializer


class UserAddress(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer








