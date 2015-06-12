from rest_framework import generics
from main.serializers import UserDetailSerializer
from main.main_models.user import ShopUser

# TODO: Convert urls to point to user_account/userview as it is essentially the same view but dosen't need PK to get the user details
# Using PK is generally a bad idea as it may allow other users to access another users account details
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopUser.objects.all()
    serializer_class = UserDetailSerializer