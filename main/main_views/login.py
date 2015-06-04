from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth import login, logout
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView

from main.serializers import ShopUserSerializer


class Login(GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=self.request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors)
        user = serializer.validated_data['user']
        login(self.request, user)
        user_serializer = ShopUserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

class Logout(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        logout(request)
        return Response({"success": "Logged out."}, status=status.HTTP_200_OK)