from rest_framework import generics, permissions
from main.models import ShopUser
from main.serializers import ShopUserSerializer

class UserView(generics.RetrieveUpdateAPIView):
    """
    Use this endpoint to retrieve/update user.
    """
    model = ShopUser
    serializer_class = ShopUserSerializer
    #permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, *args, **kwargs):
        return self.request.user
